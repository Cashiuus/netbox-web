from django.apps import AppConfig


class WIMConfig(AppConfig):
    name = "wim"
    verbose_name = "WIM"

    def ready(self):
        from . import signals, search
