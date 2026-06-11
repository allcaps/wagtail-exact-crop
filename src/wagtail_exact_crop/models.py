from django.db import models


class ExactCropImageMixin(models.Model):
    exact_crops = models.JSONField(blank=True, default=dict)

    class Meta:
        abstract = True
