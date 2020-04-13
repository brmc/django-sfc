import os
import uuid
from pathlib import Path

from django.apps import apps
from django.contrib.staticfiles import finders
from django.core.management.base import BaseCommand

from sfc.register import registry


def create_file(content: str, name, ext):
    directory = name.parent
    name = str(name) + ext
    os.makedirs(directory, exist_ok=True)
    with open(name, 'w+') as output:
        print(f"File written to {name}")
        output.write(content)


class Command(BaseCommand):
    help = "Searches the single-file-component registry"

    def handle(self, *args, **options):
        while finders.find(uuid.uuid1().bytes.__str__()):
            # There's got to be a better way to find static directories
            pass
        static_dirs = finders.searched_locations
        app_dirs = [a.path for a in apps.get_app_configs()]
        static_dir_map = {ad: sd for ad in app_dirs for sd in static_dirs if sd.startswith(ad)}
        for name, tpl in registry.templates.items():
            matching_app_dirs = [a for a in app_dirs if tpl.origin.name.startswith(a)]
            if not matching_app_dirs:
                raise Exception(f"No matching app dirs were found for this template: {tpl.name}")
            try:
                while not (static_dir := static_dir_map.get(matching_app_dirs.pop())):
                    pass
            except IndexError as e:
                raise Exception(f"No static directory found for the app that contains {tpl.name}. Did you forget to "
                                f"create it?")
            file_name = Path(static_dir) / tpl.file_name
            if js := tpl.js.render():
                create_file(js, file_name, '.js')
            if css := tpl.css.render():
                create_file(css, file_name, '.css')
