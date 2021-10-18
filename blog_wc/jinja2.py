from django_jinja import library
from django.urls import translate_url
from django.conf import settings

from apps.blog.models import Article


@library.global_function
def get_lang_urls(request):
    current_url = request.build_absolute_uri()
    return [(code, name, translate_url(current_url, code)) for code, name in settings.LANGUAGES]

@library.global_function
def get_new_articles(request):
    qs = Article.objects.order_by('-create_date').exclude(author=request.user).select_related('author', 'category')
    return qs[:9]