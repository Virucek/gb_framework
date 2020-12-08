import os

from jinja2 import Template


def render(template_name, **kwargs):
    file = os.path.join('templates', template_name)
    with open(file, encoding='utf-8') as file:
        template = Template(file.read())
    return template.render(**kwargs)
