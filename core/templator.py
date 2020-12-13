import os

from jinja2 import Template, Environment, FileSystemLoader


def render(template_name, folder='templates', **kwargs):
    # file = os.path.join('templates', template_name)
    # with open(file, encoding='utf-8') as file:
    #     template = Template(file.read())
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    if 'context' in kwargs:  # Если в качестве аргумент был передан context - используется именно он.
        return template.render(**kwargs['context'])
    return template.render(**kwargs)
