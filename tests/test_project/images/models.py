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
        "exact_crops",
    )


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage,
        on_delete=models.CASCADE,
        related_name="renditions",
    )

    class Meta:
        unique_together = (
            ("image", "filter_spec", "focal_point_key"),
        )
