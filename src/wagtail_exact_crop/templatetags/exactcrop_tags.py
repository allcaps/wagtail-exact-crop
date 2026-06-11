from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

register = template.Library()


@register.inclusion_tag("exactcrop/crop_widgets.html", takes_context=True)
def exact_crop_widgets(context):
    """
    Renders crop widgets for the given image in the edit view.
    Flattens presets + widgets into a simple list of dicts for easy template use.
    """

    presets = getattr(settings, "WAGTAIL_EXACT_IMAGE_CROP_PRESETS", {})
    widgets = getattr(settings, "WAGTAIL_EXACT_IMAGE_CROP_WIDGETS", {})

    original_image = context.get("original_image")

    widget_list = []
    for widget_name, widget in widgets.items():
        preset_keys = widget.get("presets", [])

        # The base preset is the one with the largest width.
        # This to avoid up-scaling in the crop widget.
        base_preset = None
        max_width = 0
        for key in preset_keys:
            preset = presets.get(key)
            if not preset:
                raise ImproperlyConfigured(
                    f"WAGTAIL_EXACT_IMAGE_CROP_WIDGETS[{widget_name!r}] references "
                    f"unknown preset {key!r}."
                )
            if preset["width"] > max_width:
                base_preset = preset
                max_width = preset["width"]

        if base_preset is None:
            raise ImproperlyConfigured(
                f"WAGTAIL_EXACT_IMAGE_CROP_WIDGETS[{widget_name!r}] must define at least one preset."
            )

        width = base_preset["width"]
        height = base_preset["height"]

        widget_list.append({
            "name": widget_name,
            "title": widget.get("title", widget_name),
            "description": widget.get("description", ""),
            "presets": preset_keys,
            "presets_str": ",".join(preset_keys),
            "width": width,
            "height": height,
            "image_url": original_image.file.url if original_image else "",
        })

    return {
        "widgets": widget_list,
    }
