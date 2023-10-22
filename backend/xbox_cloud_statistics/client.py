import asyncio
import functools
from datetime import datetime, timezone

import httpx
import msal

from xbox_cloud_statistics.models import Game, Measurement, Region, Subscription

CONCURRENCY = 10
SCOPES = ["xboxlive.signin", "xboxlive.offline_access"]


def limit(concurrency):
    semaphore = asyncio.Semaphore(concurrency)

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            async with semaphore:
                return await func(*args, **kwargs)

        return wrapper

    return decorator


class XBoxCloudClient:
    def __init__(
        self, http_client: httpx.AsyncClient, client_id: str, client_secret: str
    ):
        self._http_client = http_client
        self._client_id = client_id
        self._client_secret = client_secret

    async def login(self, account_type: Subscription, refresh_token: str):
        access_token = self._get_oauth_token(refresh_token)
        xbox_live_token = await self._get_xbox_live_token(access_token)
        xsts_token = await self._get_xsts_token(xbox_live_token)

        offeringId = "xgpuweb"
        if account_type == Subscription.F2P:
            offeringId += "f2p"

        url = f"https://{offeringId}.gssv-play-prod.xboxlive.com/v2/login/user"
        data = {"offeringId": offeringId, "token": xsts_token}
        response = await self._http_client.post(url, json=data)
        response.raise_for_status()

        json = response.json()

        self.gs_token = json.get("gsToken")
        self.regions = [
            Region(
                name=region.get("name"),
                url=region.get("baseUri"),
            )
            for region in json.get("offeringSettings").get("regions")
        ]

    @limit(CONCURRENCY)
    async def measure(self, region: Region, game: Game) -> Measurement:
        response = await self._http_client.get(
            f"{region.url}/v1/waittime/{game.id}",
            headers={"Authorization": f"Bearer {self.gs_token}"},
        )
        response.raise_for_status()

        server_time = datetime.strptime(
            response.headers.get("Date"), "%a, %d %b %Y %H:%M:%S %Z"
        ).replace(tzinfo=timezone.utc)

        wait_time = response.json().get("estimatedTotalWaitTimeInSeconds")

        return Measurement(server_time, wait_time)

    def _get_oauth_token(self, refresh_token: str):
        app = msal.ConfidentialClientApplication(
            client_id=self._client_id,
            client_credential=self._client_secret,
            authority="https://login.microsoftonline.com/consumers",
        )

        access_token = app.acquire_token_by_refresh_token(
            refresh_token=refresh_token, scopes=SCOPES
        ).get("access_token")

        return access_token

    async def _get_xbox_live_token(self, access_token: str):
        url = "https://user.auth.xboxlive.com/user/authenticate"
        headers = {"x-xbl-contract-version": "1"}
        data = {
            "Properties": {
                "AuthMethod": "RPS",
                "RpsTicket": f"d={access_token}",
                "SiteName": "user.auth.xboxlive.com",
            },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
        }

        response = await self._http_client.post(url, headers=headers, json=data)
        response.raise_for_status()

        return response.json().get("Token")

    async def _get_xsts_token(self, token: str):
        url = "https://xsts.auth.xboxlive.com/xsts/authorize"
        headers = {"x-xbl-contract-version": "1"}
        data = {
            "Properties": {
                "SandboxId": "RETAIL",
                "UserTokens": [token],
            },
            "RelyingParty": "http://gssv.xboxlive.com/",
            "TokenType": "JWT",
        }
        response = await self._http_client.post(url, headers=headers, json=data)
        response.raise_for_status()

        return response.json().get("Token")
