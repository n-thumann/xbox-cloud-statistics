from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from jinja2 import Environment, FileSystemLoader, StrictUndefined

DIST = Path("./dist")


class Templates:
    def __init__(self) -> None:
        environment = Environment(
            loader=FileSystemLoader(Path(__file__).parent),
            undefined=StrictUndefined,
        )

        environment.filters["format_seconds"] = lambda seconds: datetime.fromtimestamp(
            seconds, tz=timezone.utc
        ).strftime("%H:%M:%S")
        environment.filters["format_date"] = lambda datetime: datetime.strftime(
            "%d/%m/%Y, %H:%M:%S %Z"
        )
        environment.filters["to_color"] = lambda subscription: (
            "#24d292" if subscription == "F2P" else "#d558c8"
        )

        self.environment = environment

    def render(self, template_name: str, output_file_name: str, **kwargs: Any):
        template = self.environment.get_template(f"{template_name}.html")
        content = template.render(**kwargs)

        output_file = (DIST / output_file_name).with_suffix(".html")
        output_file.parent.mkdir(exist_ok=True)
        output_file.write_text(content)
