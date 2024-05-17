from datetime import datetime, timezone
import json
from pathlib import Path
from influxdb_client import Point, WriteOptions, WritePrecision

from common.config import Config


from influxdb_client import InfluxDBClient


def run():
    points = []
    for game in Path("results/games").iterdir():
        if not game.is_dir():
            continue

        for region in sorted(game.iterdir()):
            if not region.is_dir():
                continue

            for subscription in region.iterdir():
                measurements = json.loads(subscription.read_text())
                for server_time, wait_time in measurements.items():
                    points.append(
                        Point("measurement")
                        .tag("game", game.name)
                        .tag("region", region.name)
                        .tag("subscription", subscription.stem)
                        .time(datetime.fromtimestamp(int(server_time), tz=timezone.utc))
                        .field("wait_time", int(wait_time))
                    )

    print(f"Loaded {len(points)} points")

    config = Config()
    with InfluxDBClient(
        url=config.influxdb_url, token=config.influxdb_token, org=config.influxdb_org
    ) as client:
        with client.write_api(
            write_options=WriteOptions(batch_size=1_000, flush_interval=500)
        ) as write_api:
            write_api.write(
                bucket=config.influxdb_bucket,
                org=config.influxdb_org,
                record=points,
                write_precision=WritePrecision.S,
            )

        tables = client.query_api().query(
            'from(bucket: "xbox-cloud-statistics") |> range(start: 0) |> group() |> count()'
        )
        count = tables[0].records[0].get_value()
        print(f"The bucket now contains {count} points")
