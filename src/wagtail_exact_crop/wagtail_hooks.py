from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from wagtail import hooks
from wagtail.images.image_operations import FilterOperation


class ExactCropOperation(FilterOperation):
    """
    Usage:

        {% image img exact-PRESET %}
    """
    vary_fields = ("exact_crops", )

    def construct(self, preset):
        self.preset = preset

    def run(self, willow, image, env):
        crop_presets = getattr(settings, "WAGTAIL_EXACT_IMAGE_CROP_PRESETS", {})
        target_size = crop_presets.get(self.preset)
        if target_size is None:
            raise ImproperlyConfigured(
                f"No WAGTAIL_EXACT_IMAGE_CROP_PRESETS entry exists for {self.preset!r}."
            )

        exact_crops = getattr(image, "exact_crops", {}) or {}
        if crop := exact_crops.get(self.preset):
            x = crop.get("x")
            y = crop.get("y")
            w = crop.get("w")
            h = crop.get("h")

            left = int(x * image.width)
            top = int(y * image.height)
            right = int((x + w) * image.width)
            bottom = int((y + h) * image.height)

            width = target_size.get("width")
            height = target_size.get("height")

            willow.image = willow.image.crop((left, top, right, bottom)).resize((width, height))
        else:
            # TODO, implement fallback
            ...
        return willow


@hooks.register("register_image_operations")
def register_image_operations():
    return [
        ("exact", ExactCropOperation),
    ]
