from django.shortcuts import render
from wagtail.images import get_image_model


def exact_crop_view(request):
    image = get_image_model().objects.order_by("pk").last()

    return render(
        request,
        "demo_app/exact_crop.html",
        {
            "img": image,
        },
    )


def focal_point_view(request):
    image = get_image_model().objects.order_by("pk").last()

    return render(
        request,
        "demo_app/focal_point.html",
        {
            "img": image,
        },
    )

