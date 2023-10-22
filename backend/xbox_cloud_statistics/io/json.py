import json
from datetime import datetime
from pathlib import Path

from xbox_cloud_statistics.io.io import IO
from xbox_cloud_statistics.models import Measurements, Model, Results

META_FILE_NAME = "meta.json"


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Model):
            return o.to_dict()
        return super().default(o)


class JSON(IO):
    @staticmethod
    def handle(results: Results, output: Path):
        output.mkdir(exist_ok=True)

        JSON._write_measurments_files(results, output)
        JSON._write_meta_file(results, output)

    @staticmethod
    def _write_measurments_files(results: Results, output: Path):
        for game, regions in results:
            for region, subscriptions in regions:
                for subscription, new_measurements in subscriptions:
                    directories = output / "games" / game.id / region.name
                    directories.mkdir(parents=True, exist_ok=True)

                    path = directories / f"{subscription.name}.json"
                    file_exists = path.exists()
                    path.touch(exist_ok=True)

                    with path.open("r+") as file:
                        if file_exists:
                            content = json.load(file)
                            measurements = Measurements.from_dict(content)
                            measurements.extend(new_measurements)
                        else:
                            measurements = new_measurements

                        file.seek(0)
                        file.truncate(0)

                        json.dump(measurements, file, cls=CustomJSONEncoder)

    @staticmethod
    def _write_meta_file(results: Results, output: Path):
        with (output / META_FILE_NAME).open("w") as file:
            content = {
                "last_update": int(datetime.now().timestamp()),
                "games": [game for game, _ in results],
            }

            file.write(json.dumps(content, cls=CustomJSONEncoder))
