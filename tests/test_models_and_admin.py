from io import BytesIO

import pytest
from django.core.files.base import ContentFile
from django.test import override_settings
from django.template.loader import render_to_string
from django.urls import reverse
from PIL import Image
from wagtail.images import get_image_model
from wagtail.models import Collection


def make_png(width=100, height=100):
    buffer = BytesIO()
    Image.new("RGB", (width, height), color="red").save(buffer, format="PNG")
    return buffer.getvalue()


@pytest.fixture
def test_image(db):
    return get_image_model().objects.create(
        title="Test image",
        file=ContentFile(make_png(), name="test.png"),
        collection=Collection.get_first_root_node(),
        exact_crops={
            "avatar": {
                "x": 0,
                "y": 0,
                "w": 1,
                "h": 1,
            },
            "medium_shot": {
                "x": 0,
                "y": 0,
                "w": 0.5,
                "h": 1,
            },
            "list_image_small": {
                "x": 0,
                "y": 0.125,
                "w": 1,
                "h": 0.75,
            },
            "list_image_medium": {
                "x": 0,
                "y": 0.125,
                "w": 1,
                "h": 0.75,
            },
            "hero_image": {
                "x": 0,
                "y": 0.3125,
                "w": 1,
                "h": 0.375,
            },
        },
    )


@pytest.mark.django_db
def test_custom_image_model_persists_exact_crops(test_image):
    image = get_image_model().objects.get(pk=test_image.pk)

    assert image.exact_crops["avatar"]["w"] == 1


@pytest.mark.django_db
def test_admin_image_edit_template_renders_for_superuser(client, django_user_model, test_image):
    user = django_user_model.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="password",
    )
    client.force_login(user)

    response = client.get(reverse("wagtailimages:edit", args=[test_image.pk]))

    assert response.status_code == 200
    assert b"exactcrop/main.js" in response.content
    assert b"exactcrop/styles.css" in response.content
    assert b'type="hidden" name="exact_crops"' in response.content
    assert b'<textarea name="exact_crops"' not in response.content
    assert b'class="focal-point-chooser"' in response.content
    assert b"show-transparency" in response.content
    assert b"focal-point-chooser.js" not in response.content
    assert b"jquery.Jcrop.min.js" not in response.content
    assert b"data-focal-point-x" not in response.content
    assert b"current-focal-point-indicator" not in response.content
    assert b"remove-focal-point" not in response.content
    assert b'name="focal_point_x"' in response.content
    assert b'name="focal_point_y"' in response.content
    assert b'name="focal_point_width"' in response.content
    assert b'name="focal_point_height"' in response.content


@pytest.mark.django_db
@override_settings(WAGTAIL_EXACT_IMAGE_CROP_FOCAL_POINT_ENABLED=True)
def test_admin_image_edit_template_can_enable_focal_point(client, django_user_model, test_image):
    user = django_user_model.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="password",
    )
    client.force_login(user)

    response = client.get(reverse("wagtailimages:edit", args=[test_image.pk]))

    assert response.status_code == 200
    assert b"focal-point-chooser.js" in response.content
    assert b"jquery.Jcrop.min.js" in response.content
    assert b"data-focal-point-x" in response.content
    assert b"current-focal-point-indicator" in response.content
    assert b"remove-focal-point" in response.content


@pytest.mark.django_db
def test_crop_widget_template_includes_static_assets(test_image):
    html = render_to_string(
        "exactcrop/crop_widgets.html",
        {
            "widgets": [
                {
                    "name": "avatar",
                    "title": "Avatar",
                    "description": "Square profile image",
                    "presets": ["avatar"],
                    "presets_str": "avatar",
                    "width": 300,
                    "height": 300,
                    "image_url": test_image.file.url,
                }
            ]
        },
    )

    assert "exactcrop/main.js" in html
    assert "exactcrop/styles.css" in html


@pytest.mark.django_db
def test_exact_crop_demo_view_renders_documented_filters(client, test_image):
    response = client.get(reverse("exact_crop_demo"))

    assert response.status_code == 200
    assert b"exact-avatar" in response.content
    assert b"exact-medium_shot" in response.content
    assert b"exact-list_image_small" in response.content
    assert b"exact-list_image_medium" in response.content
    assert b"exact-hero_image" in response.content


@pytest.mark.django_db
def test_focal_point_demo_view_renders_fill_filters(client, test_image):
    response = client.get(reverse("focal_point_demo"))

    assert response.status_code == 200
    assert b"fill-300x300" in response.content
    assert b"fill-400x800" in response.content
    assert b"fill-400x300" in response.content
    assert b"fill-800x600" in response.content
    assert b"fill-1600x600" in response.content
