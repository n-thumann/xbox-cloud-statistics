from pathlib import Path
from site_generator.providers.provider import Provider
import pytailwindcss

TAILWIND_VERSION = "v3.4.1"


class CSS(Provider):
    def get(self) -> list[str]:
        css = pytailwindcss.run(
            tailwindcss_cli_args=[
                "-c",
                "templates/tailwind.config.js",
                "--minify",
                "-i",
                "templates/tailwind.css",
            ],
            cwd=Path(__file__).parent.parent,
            auto_install=True,
            version=TAILWIND_VERSION,
        )

        return [css]
