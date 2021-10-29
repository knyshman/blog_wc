import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

AUTH_USER_MODEL = 'accounts.MyUser'

SECRET_KEY = os.getenv('SECRET_KEY')
SECRET_KEY = SECRET_KEY
DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'modeltranslation',
    'rosetta',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'ckeditor',
    'ckeditor_uploader',
    'adminsortable2',
    'apps.accounts',
    'apps.blog',
    'apps.menu',
    'django_filters',
    'django_starfield',
    'treebeard',
    'django_jinja',
    'bootstrapform_jinja',
    'django_cleanup',
    'rest_framework',
    'storages',
    'django_celery_beat'
]
SITE_ID = 2
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'blog_wc.urls'

TEMPLATES = [
    {'BACKEND': 'django_jinja.backend.Jinja2',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': False,
        'OPTIONS': {
            'match_extension': '.html',
            'extensions': [
                "jinja2.ext.do",
                "jinja2.ext.loopcontrols",
                'jinja2.ext.i18n',
                'jinja2.ext.with_',
                "django_jinja.builtins.extensions.CsrfExtension",
                'django_jinja.builtins.extensions.CacheExtension',
                "django_jinja.builtins.extensions.DebugExtension",
                'django_jinja.builtins.extensions.TimezoneExtension',
                "django_jinja.builtins.extensions.UrlsExtension",
                "django_jinja.builtins.extensions.StaticFilesExtension",
                "django_jinja.builtins.extensions.DjangoFiltersExtension",

            ],
            "globals": {
                'available_languages': 'blog_wc.jinja2.get_lang_urls',
                'recommended': 'blog_wc.jinja2.get_new_articles',
                'str_time': 'blog_wc.jinja2.str_time',

            },
            'context_processors': [
                'django.contrib.messages.context_processors.messages',
            ],

        },
    },

    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

WSGI_APPLICATION = 'blog_wc.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# CACHES = {
#     "default":  {
#         "BACKEND":  "django_redis.cache.RedisCache",
#         "LOCATION":  "redis://127.0.0.1:6379/1",
#         "OPTIONS":  {
#             "CLIENT_CLASS":  "django_redis.client.DefaultClient",
#         }
#     }
# }


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True


ugettext_lazy = lambda s: s


LANGUAGES = (
    ('ru', ugettext_lazy('Русский')),
    ('en', ugettext_lazy('English')),
    ('uk', ugettext_lazy('Украинский')),
)
MODELTRANSLATION_TRANSLATION_FILES = (
    'apps.blog',
    'apps.accounts',
    'apps.menu'
)
ACCOUNT_ACTIVATION_DAYS = 30
DEFAULT_CHARSET = 'utf-8'
LOCALE_PATHS = (BASE_DIR, 'locale/')


ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = '/'
INTERNAL_IPS = [
    '127.0.0.1', '172.16.0.1'
]
ROSETTA_ACCESS_CONTROL_FUNCTION = lambda x: x.is_superuser

DJANGO_WYSIWYG_FLAVOR = 'ckeditor'

from dotenv import load_dotenv
load_dotenv()

#local
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'media'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440
FILE_UPLOAD_PERMISSION = 0o777

#AMAZON
# AWS_ACCESS_KEY_ID=os.getenv('AMAZON_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY=os.getenv('AMAZON_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME=os.getenv('AWS_STORAGE_BUCKET_NAME')
# AWS_URL=os.getenv('AWS_URL')
# AWS_DEFAULT_ACL = None
# AWS_S3_REGION_NAME = 'eu-north-1'
# AWS_S3_SIGNATURE_VERSION = 's3v4'
# CKEDITOR_UPLOAD_PATH = '/static/'
# STATIC_URL = '/static/'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# MEDIA_URL = AWS_URL + '/media/'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_QUERYSTRING_AUTH = False


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Kiev'
CELERY_SEND_EVENTS = True
CELERY_RESULT_SERIALIZER = 'json'
MAILQUEUE_CELERY = True

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}