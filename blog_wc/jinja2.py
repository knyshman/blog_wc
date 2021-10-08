from django_jinja import library
from django.urls import translate_url
from django.conf import settings


@library.global_function
def get_lang_urls(request):
    current_url = request.build_absolute_uri()
    return [(code, name, translate_url(current_url, code)) for code, name in settings.LANGUAGES]