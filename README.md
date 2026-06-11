# Wagtail Exact Crop

Exact image cropping for Wagtail.

## Installation

```shell
pip install wagtail-exact-crop
```

Add `wagtail_exact_crop` to installed apps:

```python
INSTALLED_APPS = [
    "wagtail_exact_crop",
    ...
]
```

Configure a custom image model with the `exact_crops` field:

```python
# images/models.py
from django.db import models
from wagtail.images.models import AbstractImage, AbstractRendition
from wagtail_exact_crop.models import ExactCropImageMixin


class CustomImage(ExactCropImageMixin, AbstractImage):
    admin_form_fields = (
        "title",
        "file",
        "description",
        "collection",
        "tags",
        "focal_point_x",
        "focal_point_y",
        "focal_point_width",
        "focal_point_height",
        "exact_crops",  # !
    )


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage,
        on_delete=models.CASCADE,
        related_name="renditions",
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)
```

Define the custom image model in your settings:

```python
# settings.py
WAGTAILIMAGES_IMAGE_MODEL = "images.CustomImage"
```

After adding the model, run `makemigrations` and `migrate`.

Define crop sizes:

```python
WAGTAIL_EXACT_IMAGE_CROP_PRESETS = {
    "avatar": {"width": 300, "height": 300},
    "medium_shot": {"width": 400, "height": 800},
    "list_image_small": {"width": 400, "height": 300},
    "list_image_medium": {"width": 800, "height": 600},
    "hero_image": {"width": 1600, "height": 600},
}
```

Define widgets (admin interface). Note that images with the same aspect ratio might share widget:

```python
WAGTAIL_EXACT_IMAGE_CROP_WIDGETS = {
    "avatar": {
        "title": "Avatar image",
        "description": "Used in listings and teasers",
        "presets": ["avatar"],
    },
    "medium_shot": {
        "title": "Medium shot image",
        "description": "Used in listings and teasers",
        "presets": ["medium_shot"],
    },
    "list_image": {
        "title": "List image",
        "description": "Used in listings and teasers",
        "presets": ["list_image_small", "list_image_medium"],
    },
    "hero_image": {
        "title": "Hero image",
        "description": "Large banner at top of page",
        "presets": ["hero_image"],
    },
}
```

Exact crop is registered as a custom image filter, so you can use it in your templates like any other image filter.
https://docs.wagtail.org/en/latest/extending/custom_image_filters.html

Just use the `exact-` prefix followed by the crop preset name to apply the crop:

```html
{% load wagtailimages_tags %}

{% image some_image exact-avatar %}
{% image some_image exact-medium_shot %}
{% image some_image exact-list_image_small %}
{% image some_image exact-list_image_medium %}
{% image some_image exact-hero_image %}
```

## Development and testing

Install the package with test dependencies:

```shell
uv venv
source .venv/bin/activate
pip install -e ".[test]"
```

Run the automated tests:

```shell
pytest
```

## Demo project

The `tests/test_project` Django/Wagtail project can be used for manual testing and demonstration.

```shell
python tests/test_project/manage.py migrate
python tests/test_project/manage.py createsuperuser
python tests/test_project/manage.py runserver
```

Then open `http://127.0.0.1:8000/admin/`, upload an image, edit it, adjust the exact crop widgets, and save.
The exact crop demo at `http://127.0.0.1:8000/exact-crop/` renders the latest uploaded image using the documented `exact-*` filters.
The focal point comparison page at `http://127.0.0.1:8000/focal-point/` renders the same target sizes with Wagtail's `fill-*` filters.

## Releasing

Releases are published to PyPI by GitHub Actions when a `v*` tag is pushed.

```shell
uv version 0.1.1
git add pyproject.toml
git commit -m "Release 0.1.1"
git tag -a v0.1.1 -m v0.1.1
git push
git push origin v0.1.1
```

The Git tag should be the package version with a `v` prefix. For example, `version = "0.1.1"` in `pyproject.toml` is released with tag `v0.1.1`.

You can also create the GitHub Release in the web UI after pushing the tag. If you create the tag through the GitHub Release UI, make sure the version bump commit is already on the target branch.

To build and inspect the package locally:

```shell
uv build
```

This writes the release artifacts to `dist/`. Before publishing, inspect the generated files and verify the package data is included:

```shell
tar -tf dist/wagtail_exact_crop-*.tar.gz
unzip -l dist/wagtail_exact_crop-*.whl
```
