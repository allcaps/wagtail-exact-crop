from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import PermissionDenied
from django.urls import path

from wagtail import hooks
from wagtail.admin.views.generic import EditView
from wagtail.images import get_image_model
from wagtail.images.image_operations import FilterOperation
from wagtail.images.permissions import permission_policy


class CropView(EditView):
    pk_url_kwarg = "image_id"
    template_name = "exactcrop/edit.html"
    model = get_image_model()
    index_url_name = "wagtailimages:index"
    edit_url_name = "crop"
    header_icon = "image"

    def get_form_class(self):
        return forms.modelform_factory(
            get_image_model(),
            fields=("exact_crops",),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["image"] = self.object
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not permission_policy.user_has_permission_for_instance(
            self.request.user, "change", obj
        ):
            raise PermissionDenied
        return obj


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path("images/<int:image_id>/crop/", CropView.as_view(), name="crop"),
    ]


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
