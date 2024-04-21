import asyncio
import itertools
from pathlib import Path

import httpx

from xbox_cloud_statistics.client import XBoxCloudClient
from xbox_cloud_statistics.config import Config
from xbox_cloud_statistics.io.cli import CLI
from xbox_cloud_statistics.io.influxdb import InfluxDB

from .models import (
    Game,
    Measurement,
    Results,
    Subscription,
)


def run():
    asyncio.run(main())


async def main():
    config = Config()
    results = Results()

    async with httpx.AsyncClient(http2=True) as http_client:
        client = XBoxCloudClient(http_client, config.client_id, config.client_secret)

        if config.f2p_token:
            await run_measurements(
                client,
                Subscription.F2P,
                config.f2p_token,
                config.f2p_games,
                results,
            )
        if config.gpu_token:
            await run_measurements(
                client,
                Subscription.GPU,
                config.gpu_token,
                config.gpu_games,
                results,
            )

    CLI.handle(results)
    InfluxDB.handle(config.influxdb_url, config.influxdb_token, config.influxdb_org, config.influxdb_bucket, results)


async def run_measurements(
    client: XBoxCloudClient,
    subscription: Subscription,
    token: str,
    games: list[Game],
    results: Results,
):
    await client.login(subscription, token)

    games_regions = list(itertools.product(games, client.regions))
    coroutines = [client.measure(region, game) for game, region in games_regions]
    times: list[Measurement | Exception] = await asyncio.gather(
        *coroutines,
        return_exceptions=True,
    )

    for task, measurement in zip(games_regions, times):
        game, region = task

        if isinstance(measurement, Exception):
            print(f"Failed to handle {game.id}@{region.name}: {measurement}")
            continue

        results[game][region][subscription] = measurement


if __name__ == "__main__":
    run()
