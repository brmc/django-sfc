import os

from django.core.management.base import BaseCommand
from django.template import Template, Context
from django.template.loaders.app_directories import get_app_template_dirs

template = Template("""\
from django import template

from sfc.templatetags.sfc import load

register = template.Library()
{% for widget in widgets %}
register.simple_tag(func=load('{{ widget.tpl }}'), name='{{ widget.name }}')
{% endfor %}
""")


class Command(BaseCommand):
    help = "Searches the single-file-component registry"

    def handle(self, *args, **options):
        for template_dir in get_app_template_dirs('templates/sfc'):
            widgets = []
            for dir_, dirs, filenames in os.walk(template_dir):
                root, _, relative = dir_.partition('templates')
                tag_library = relative.lstrip(os.path.sep)
                tag_library_file = "_".join(tag_library.split(os.path.sep)) + '.py'
                for filename in filenames:
                    widget_name = filename.replace('.html', '')
                    tpl = os.path.join(tag_library, filename)
                    widgets.append(dict(tpl=tpl, name=widget_name))
                    print(f"{widget_name} registered in {tag_library_file}")
                tag_dir = os.path.join(root, 'templatetags', tag_library_file)
                if not widgets:
                    continue
                with open(tag_dir, 'w+') as file:
                    print(f"{tag_library_file} written to {tag_dir}")
                    file.write(template.render(Context(dict(widgets=widgets))))
