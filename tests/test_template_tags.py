from types import SimpleNamespace

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from wagtail_exact_crop.templatetags.exactcrop_tags import exact_crop_widgets


def test_exact_crop_widgets_builds_widget_context():
    original_image = SimpleNamespace(file=SimpleNamespace(url="/media/example.jpg"))

    context = exact_crop_widgets({"original_image": original_image})

    assert context["widgets"] == [
        {
            "name": "avatar",
            "title": "Avatar image",
            "description": "Used in listings and teasers",
            "presets": ["avatar"],
            "presets_str": "avatar",
            "width": 300,
            "height": 300,
            "image_url": "/media/example.jpg",
        },
        {
            "name": "medium_shot",
            "title": "Medium shot image",
            "description": "Used in listings and teasers",
            "presets": ["medium_shot"],
            "presets_str": "medium_shot",
            "width": 400,
            "height": 800,
            "image_url": "/media/example.jpg",
        },
        {
            "name": "list_image",
            "title": "List image",
            "description": "Used in listings and teasers",
            "presets": ["list_image_small", "list_image_medium"],
            "presets_str": "list_image_small,list_image_medium",
            "width": 800,
            "height": 600,
            "image_url": "/media/example.jpg",
        },
        {
            "name": "hero_image",
            "title": "Hero image",
            "description": "Large banner at top of page",
            "presets": ["hero_image"],
            "presets_str": "hero_image",
            "width": 1600,
            "height": 600,
            "image_url": "/media/example.jpg",
        },
    ]


@override_settings(
    WAGTAIL_EXACT_IMAGE_CROP_WIDGETS={
        "broken": {
            "title": "Broken",
            "presets": ["missing"],
        }
    }
)
def test_exact_crop_widgets_raises_for_unknown_preset():
    with pytest.raises(ImproperlyConfigured, match="unknown preset 'missing'"):
        exact_crop_widgets({})


@override_settings(
    WAGTAIL_EXACT_IMAGE_CROP_WIDGETS={
        "empty": {
            "title": "Empty",
            "presets": [],
        }
    }
)
def test_exact_crop_widgets_raises_for_widget_without_presets():
    with pytest.raises(ImproperlyConfigured, match="must define at least one preset"):
        exact_crop_widgets({})
