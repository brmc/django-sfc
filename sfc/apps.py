from django.apps import AppConfig

from sfc.register import registry


class SfcConfig(AppConfig):
    name = 'sfc'

    def ready(self):
        registry.register('')
