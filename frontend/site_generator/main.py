from collections import defaultdict
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path

from site_generator.providers.css import CSS
from site_generator.providers.font import Font
from site_generator.providers.js import JS
from site_generator.templates.templates import Templates

MINIMUM_TIMESTAMP = (datetime.now() - timedelta(days=3)).timestamp()


def main():
    templates = Templates()
    meta = json.loads(Path("results/meta.json").read_text())
    games_meta = meta.get("games")
    games = get_games()

    defaults = {
        "scripts": JS().get(),
        "styles": [*Font().get(), *CSS().get()],
        "last_update": datetime.fromtimestamp(meta.get("last_update"), tz=timezone.utc),
    }

    write_index(templates, defaults, games_meta)
    write_games(templates, defaults, games_meta, games)


def write_index(template: Templates, defaults: dict, games_meta: list):
    template.render("index", "index", **defaults, games=games_meta)


def write_games(template: Templates, defaults: dict, games_meta: list, games: dict):
    for game in games_meta:
        id = game.get("id")
        title = game.get("title")
        results = games.get(id)

        template.render("game", f"games/{id}", **defaults, title=title, results=results)


def get_games():
    games = defaultdict(lambda: defaultdict(dict))
    for game in Path("results/games").iterdir():
        for region in sorted(game.iterdir()):
            for subscription in region.iterdir():
                measurements = {
                    k: v
                    for k, v in json.loads(subscription.read_text()).items()
                    if int(k) > MINIMUM_TIMESTAMP
                }
                games[game.name][region.name][subscription.stem] = measurements

    return games


if __name__ == "__main__":
    main()
