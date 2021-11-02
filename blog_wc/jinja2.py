from django_jinja import library
from django.urls import translate_url
from django.conf import settings
from apps.blog.models import Article
from apps.menu.models import Menu, TextPage


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
        qs = qs.exclude(author=request.user)
    return qs[:9].prefetch_related('comment_set')


@library.global_function
def str_time(date):
    return date.strftime("%d.%m.%Y, %H:%M")


@library.global_function
def get_header():
    header = Menu.objects.filter(position=0, is_active=1)
    return header


@library.global_function
def get_footer():
    footer = Menu.objects.filter(position=1, is_active=1)
    return footer


@library.global_function
def get_textpages():
    texpages = TextPage.objects.all()
    return texpages

