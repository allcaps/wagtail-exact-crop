from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from .demo_app.views import exact_crop_view, focal_point_view

urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("exact-crop/", exact_crop_view, name="exact_crop_demo"),
    path("focal-point/", focal_point_view, name="focal_point_demo"),
    path("", include(wagtail_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
