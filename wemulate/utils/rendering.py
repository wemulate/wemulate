import os
from typing import Dict, List, Text

from jinja2 import Environment, FileSystemLoader
from jinja2.environment import Template

from wemulate.core.database.models import ParameterModel


def rendering(data: Dict[str, List[ParameterModel]], template_file_name: str) -> Text:
    env: Environment = Environment(
        loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), "../templates")
        ),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template: Template = env.get_template(template_file_name)
    return template.render(data)
