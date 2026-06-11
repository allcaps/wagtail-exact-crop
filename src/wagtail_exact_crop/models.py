from django import forms
from django.db import models


class ExactCropsField(models.JSONField):
    def formfield(self, **kwargs):
        kwargs.setdefault("widget", forms.HiddenInput)
        return super().formfield(**kwargs)


class ExactCropImageMixin(models.Model):
    exact_crops = ExactCropsField(blank=True, default=dict)

    class Meta:
        abstract = True
