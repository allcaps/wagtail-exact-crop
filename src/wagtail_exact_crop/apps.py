from django.apps import AppConfig


class WagtailExactCropConfig(AppConfig):
    name = "wagtail_exact_crop"
    verbose_name = "Wagtail Exact Crop"

    def ready(self):
        from . import checks  # noqa: F401
