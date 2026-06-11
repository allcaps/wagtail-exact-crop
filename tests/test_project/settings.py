from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = "wagtail-exact-crop-test-key"
DEBUG = True
ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = "tests.test_project.urls"
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
    "tests.test_project.images",
    "tests.test_project.demo_app",
    "wagtail_exact_crop",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

WAGTAIL_SITE_NAME = "Wagtail Exact Crop Test Project"
WAGTAILADMIN_BASE_URL = "http://127.0.0.1:8000"
WAGTAILIMAGES_IMAGE_MODEL = "images.CustomImage"

WAGTAIL_EXACT_IMAGE_CROP_PRESETS = {
    "avatar": {"width": 300, "height": 300},
    "medium_shot": {"width": 400, "height": 800},
    "list_image_small": {"width": 400, "height": 300},
    "list_image_medium": {"width": 800, "height": 600},
    "hero_image": {"width": 1600, "height": 600},
}

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
