from typing import Dict
from jinja2 import Environment, FileSystemLoader
from jinja2.environment import Template


def rendering(data : Dict, template_file_name : str) -> str:
    env : Environment = Environment(
        loader=FileSystemLoader("./wemulate/templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template : Template = env.get_template(template_file_name)
    return template.render(data)