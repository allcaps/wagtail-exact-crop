from django.contrib.staticfiles import finders


def test_exact_crop_static_files_are_discoverable():
    assert finders.find("exactcrop/main.js")
    assert finders.find("exactcrop/styles.css")

