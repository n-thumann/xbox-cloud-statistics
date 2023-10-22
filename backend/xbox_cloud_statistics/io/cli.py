from tabulate import tabulate

from xbox_cloud_statistics.models import Results

from .io import IO


class CLI(IO):
    @staticmethod
    def handle(results: Results):
        output = []
        for game, regions in results:
            for region, subscriptions in regions:
                for subscription, measurements in subscriptions:
                    latest_measurement = measurements.latest()
                    server_time, wait_time = (
                        latest_measurement.server_time,
                        latest_measurement.wait_time,
                    )
                    output.append(
                        [game.id, region.name, subscription, server_time, wait_time]
                    )

        headers = [
            "Game",
            "Region",
            "Subscription",
            "Server time",
            "Wait time (s)",
        ]
        print(tabulate(output, headers=headers, tablefmt="github"))
