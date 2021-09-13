from typing import Dict, Text
from jinja2 import Environment, FileSystemLoader
from jinja2.environment import Template
import os


def rendering(data: Dict[str, int], template_file_name: str) -> Text:
    env: Environment = Environment(
        loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), "../templates")
        ),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template: Template = env.get_template(template_file_name)
    return template.render(data)
