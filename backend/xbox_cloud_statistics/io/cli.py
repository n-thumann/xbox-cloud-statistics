from tabulate import tabulate

from xbox_cloud_statistics.models import Results

from .io import IO


class CLI(IO):
    @staticmethod
    def handle(results: Results):
        output = []
        for game, regions in results:
            for region, subscriptions in regions:
                for subscription, measurement in subscriptions:
                    output.append(
                        [game.id, region.name, subscription, measurement.server_time, measurement.wait_time]
                    )

        headers = [
            "Game",
            "Region",
            "Subscription",
            "Server time",
            "Wait time (s)",
        ]
        print(tabulate(output, headers=headers, tablefmt="github"))
