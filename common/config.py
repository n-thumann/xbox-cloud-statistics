from functools import reduce
import operator
import os
import tomllib

from common.models import Game, Subscription


class Config:
    games: list[Game] = list()

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

        self.influxdb_url = os.environ.get("INFLUXDB_URL")
        self.influxdb_token = os.environ.get("INFLUXDB_TOKEN")
        self.influxdb_org = os.environ.get("INFLUXDB_ORG")
        self.influxdb_bucket = os.environ.get("INFLUXDB_BUCKET")

    def _validate(self):
        if not any(
            [
                self.influxdb_url,
                self.influxdb_token,
                self.influxdb_org,
                self.influxdb_bucket,
            ]
        ):
            raise Exception(
                "Environment variables for InfluxDB (INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG and INFLUXDB_BUCKET) are required"
            )