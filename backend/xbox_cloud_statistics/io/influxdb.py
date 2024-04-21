from datetime import datetime
from pathlib import Path

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from xbox_cloud_statistics.models import Measurement, Results

from .io import IO


class InfluxDB(IO):
    @staticmethod
    def handle(url: str, token: str, org: str, bucket: str, results: Results):

        points = []
        for game, regions in results:
            for region, subscriptions in regions:
                for subscription, measurement in subscriptions:
                    measurement
                    point = (
                        Point("measurement")
                        .tag("game", game.id)
                        .tag("region", region.name)
                        .tag("subscription", subscription)
                        .time(measurement.server_time)
                        .field("wait_time", measurement.wait_time)
                    )

                    points.append(point)

        with InfluxDBClient(url=url, token=token, org=org) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=bucket, org=org, record=points)
