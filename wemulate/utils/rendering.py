from jinja2 import Environment, FileSystemLoader
from jinja2.environment import Template


def rendering(data, template):
    env = Environment(
        loader=FileSystemLoader("./wemulate/templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(template)
    renderdata = template.render(data)
    return renderdata