from types import SimpleNamespace

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from wagtail_exact_crop.wagtail_hooks import ExactCropOperation


class FakeImageProcessor:
    def __init__(self):
        self.crop_box = None
        self.resize_size = None

    def crop(self, box):
        self.crop_box = box
        return self

    def resize(self, size):
        self.resize_size = size
        return self


def run_operation(preset, image):
    operation = ExactCropOperation("exact", preset)
    processor = FakeImageProcessor()
    willow = SimpleNamespace(image=processor)

    result = operation.run(willow, image, None)

    return result, processor


def test_exact_crop_operation_crops_and_resizes_from_relative_coordinates():
    image = SimpleNamespace(
        width=1000,
        height=500,
        exact_crops={
            "avatar": {
                "x": 0.1,
                "y": 0.2,
                "w": 0.4,
                "h": 0.6,
            }
        },
    )

    _, processor = run_operation("avatar", image)

    assert processor.crop_box == (100, 100, 500, 400)
    assert processor.resize_size == (300, 300)


def test_exact_crop_operation_returns_willow_when_crop_data_is_missing():
    image = SimpleNamespace(width=1000, height=500, exact_crops={})

    willow, processor = run_operation("avatar", image)

    assert willow.image is processor
    assert processor.crop_box is None
    assert processor.resize_size is None


@override_settings(WAGTAIL_EXACT_IMAGE_CROP_PRESETS={})
def test_exact_crop_operation_raises_for_unknown_preset():
    image = SimpleNamespace(width=1000, height=500, exact_crops={})

    with pytest.raises(ImproperlyConfigured, match="No WAGTAIL_EXACT_IMAGE_CROP_PRESETS"):
        run_operation("missing", image)
