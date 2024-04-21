import operator
import os
from functools import reduce

import tomllib

from xbox_cloud_statistics.models import Game, Subscription


class Config:
    def __init__(self):
        with open("config.toml", mode="rb") as fp:
            config = tomllib.load(fp)

            self.games = list()
            for id, info in config.get("games").items():
                subscriptions = reduce(
                    operator.or_,
                    map(Subscription.from_string, info.get("subscriptions")),
                )
                self.games.append(
                    Game(id, info.get("title"), info.get("image_url"), subscriptions)
                )

        self.client_id = os.environ.get("CLIENT_ID")
        self.client_secret = os.environ.get("CLIENT_SECRET")

        self.f2p_token = os.environ.get("F2P_TOKEN")
        self.gpu_token = os.environ.get("GPU_TOKEN")

        self.influxdb_url = os.environ.get("INFLUXDB_URL")
        self.influxdb_token = os.environ.get("INFLUXDB_TOKEN")
        self.influxdb_org = os.environ.get("INFLUXDB_ORG")
        self.influxdb_bucket =  os.environ.get("INFLUXDB_BUCKET")

        self._validate()

    def _validate(self):
        if not self.client_id or not self.client_secret:
            raise Exception(
                "Environment variables CLIENT_ID and CLIENT_SECRET are required"
            )

        all_subscriptions = reduce(
            operator.or_, [game.subscriptions for game in self.games]
        )

        if (Subscription.F2P in all_subscriptions) ^ bool(self.f2p_token):
            raise Exception(
                "F2P games and environment variable "
                "F2P_TOKEN need to be specified mutally"
            )

        if (Subscription.GPU in all_subscriptions) ^ bool(self.gpu_token):
            raise Exception(
                "GPU games and environment variable "
                "GPU_TOKEN need to be specified mutally"
            )
        
        if not any([self.influxdb_url, self.influxdb_token, self.influxdb_org, self.influxdb_bucket]):
            raise Exception("Environment variables for InfluxDB (INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG and INFLUXDB_BUCKET) are required")

    @property
    def f2p_games(self) -> list[Game]:
        return [game for game in self.games if Subscription.F2P in game.subscriptions]

    @property
    def gpu_games(self) -> list[Game]:
        return [game for game in self.games if Subscription.GPU in game.subscriptions]
