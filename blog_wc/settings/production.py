import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
from dotenv import load_dotenv
load_dotenv()
AUTH_USER_MODEL = 'accounts.MyUser'

SECRET_KEY = os.getenv('SECRET_KEY')
SECRET_KEY = SECRET_KEY
DB_NAME = os.environ.get('DB_NAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')

DEBUG = False

ALLOWED_HOSTS = ['knyshblog.herokuapp.com']


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
    'ckeditor',
    'ckeditor_uploader',
    'adminsortable2',
    'apps.accounts',
    'apps.blog',
    'apps.menu',
    'django_filters',
    'django_starfield',
    'treebeard',
    'debug_toolbar',
    'django_jinja',
    'bootstrapform_jinja',
    'django_cleanup',
    'rest_framework',
    'storages',
    'django_celery_beat',
    'corsheaders'
]
SITE_ID = 3
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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
                'get_header': 'blog_wc.jinja2.get_header',
                'get_footer': 'blog_wc.jinja2.get_footer',
                'textpages': 'blog_wc.jinja2.get_textpages',


            },
            'context_processors': [
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
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
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': '5432',
    }
}

import dj_database_url
db = dj_database_url.config()
DATABASES['default'].update(db)

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


CORS_ALLOW_ALL_ORIGINS = False
# #AMAZON
AWS_ACCESS_KEY_ID = os.getenv('AMAZON_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AMAZON_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_URL = os.getenv('AWS_URL')
AWS_DEFAULT_ACL = 'public-read-write'
AWS_S3_REGION_NAME = 'eu-north-1'
AWS_S3_SIGNATURE_VERSION = 's3v4'
STATIC_URL = AWS_URL + '/static/'
STATICFILES_STORAGE = 'blog_wc.storage_backends.MediaStorage'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'media'),)
MEDIA_URL = AWS_URL + '/media/'
CKEDITOR_UPLOAD_PATH = AWS_URL + '/media/'
DEFAULT_FILE_STORAGE = 'blog_wc.storage_backends.MediaStorage'
ENDPOINT_URL = AWS_URL
ACCESS_ID = AWS_ACCESS_KEY_ID

AWS_QUERYSTRING_AUTH = True
AWS_S3_SECURE_URLS = False


from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = default_headers + (
    'Access-Control-Allow-Headers',
    'Access-Control-Allow-Credentials',
    'Access-Control-Allow-Origin',
)


CORS_ORIGIN_WHITELIST = (
    'http://localhost:7000',
    'http://127.0.0.1:7000',
    'https://blogwc.s3.amazonaws.com'

)
CKEDITOR_CONFIGS = {
    "default": {
        "removePlugins": "exportpdf",
    },
    'awesome_ckeditor': {
        'toolbar': 'Basic',
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'

REDIS_URL = os.environ.get('REDIS_URL')
CELERY_BROKER_URL = REDIS_URL
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3}
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Kiev'
CELERY_SEND_EVENTS = True
CELERY_RESULT_SERIALIZER = 'json'
MAILQUEUE_CELERY = True


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.BrowsableAPIRenderer',
        'apps.blog.api.renderers.CustomRenderer',
    ]
}

# CACHES = {
#     "default":  {
#         "BACKEND":  "django_redis.cache.RedisCache",
#         "LOCATION":  REDIS_URL,
#         "OPTIONS":  {
#             "CLIENT_CLASS":  "django_redis.client.DefaultClient",
#         }
#     }
# }
