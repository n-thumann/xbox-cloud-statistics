from collections import defaultdict
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path

from common.models import Game
from site_generator.config import FrontendConfig
from site_generator.providers.css import CSS
from site_generator.providers.font import Font
from site_generator.providers.js import JS
from site_generator.templates.templates import Templates

from influxdb_client import InfluxDBClient


MINIMUM_TIMESTAMP = (datetime.now() - timedelta(days=3)).timestamp()


def main():
    config = FrontendConfig()
    templates = Templates()
    games_meta = config.games

    with InfluxDBClient(
        url=config.influxdb_url, token=config.influxdb_token, org=config.influxdb_org
    ) as client:
        games = get_games(client, config.influxdb_bucket)
        last_update = get_last_update(client, config.influxdb_bucket)

    defaults = {
        "scripts": JS().get(),
        "styles": [*Font().get(), *CSS().get()],
        "last_update": last_update,
    }

    write_index(templates, defaults, games_meta)
    write_games(templates, defaults, games_meta, games)


def write_index(template: Templates, defaults: dict, games_meta: list):
    template.render("index", "index", **defaults, games=games_meta)


def write_games(
    template: Templates, defaults: dict, games_meta: list[Game], games: dict
):
    for game in games_meta:
        results = games.get(game.id)

        template.render(
            "game", f"games/{game.id}", **defaults, title=game.title, results=results
        )


def get_games(influxdb_client: InfluxDBClient, influxdb_bucket: str):
    query_api = influxdb_client.query_api()
    tables = query_api.query(f'from(bucket:"{influxdb_bucket}") |> range(start: -14d)')

    games = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    for table in tables:
        for record in table.records:
            game = record["game"]
            region = record["region"]
            subscription = record["subscription"]

            x = int(record.get_time().timestamp())
            y = record.get_value()

            games[game][region][subscription][x] = y

    return games


def get_last_update(influxdb_client: InfluxDBClient, influxdb_bucket: str):
    query_api = influxdb_client.query_api()
    tables = query_api.query(
        f'from(bucket:"{influxdb_bucket}") |> range(start: -14d) |> keep(columns: ["_time"]) |> last(column: "_time") |> sort(columns: ["_time"], desc: false) |> limit(n: 1)'
    )
    return tables[0].records[0].get_time()


if __name__ == "__main__":
    main()
