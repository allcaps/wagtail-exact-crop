import pytest


@pytest.fixture(autouse=True)
def temporary_media_root(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path / "media"

