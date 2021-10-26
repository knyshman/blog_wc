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
    qs = Article.objects.select_related('author', 'category').filter(is_recommended=True).order_by('-create_date')
    if not request.user.is_authenticated:
        qs = qs
    else:
        qs = qs.select_related('author').exclude(author=request.user)
    return qs[:9].prefetch_related('comment_set', )


@library.global_function
def str_time(date):
    return date.strftime("%d.%m.%Y, %H:%M")

