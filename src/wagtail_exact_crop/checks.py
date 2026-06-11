from django.core.checks import Error, register

from wagtail.images import get_image_model


@register()
def check_exact_crops_field(app_configs, **kwargs):
    image_model = get_image_model()

    try:
        image_model._meta.get_field("exact_crops")
    except Exception:
        return [
            Error(
                "The Wagtail image model must define an exact_crops JSONField.",
                hint=(
                    "Inherit from wagtail_exact_crop.models.ExactCropImageMixin "
                    "on your custom image model and run migrations."
                ),
                id="wagtail_exact_crop.E001",
            )
        ]

    return []
