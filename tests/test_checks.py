from django.core.checks import Error
from django.test import override_settings

from wagtail_exact_crop.checks import check_exact_crops_field


def test_exact_crops_field_check_passes_for_custom_image_model():
    assert check_exact_crops_field(None) == []


@override_settings(WAGTAILIMAGES_IMAGE_MODEL="wagtailimages.Image")
def test_exact_crops_field_check_reports_missing_field():
    errors = check_exact_crops_field(None)

    assert errors == [
        Error(
            "The Wagtail image model must define an exact_crops JSONField.",
            hint=(
                "Inherit from wagtail_exact_crop.models.ExactCropImageMixin "
                "on your custom image model and run migrations."
            ),
            id="wagtail_exact_crop.E001",
        )
    ]

