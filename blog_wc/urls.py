from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from apps.menu.views import TextPageView
from django.conf.urls.static import static

User = get_user_model()

api_urlpatterns = [
    path('blog/', include('apps.blog.api.urls')),
]
from ckeditor_uploader import views
from django.views.decorators.cache import never_cache


ckeditor_urls = [

    re_path(r"^upload/", views.upload, name="ckeditor_upload"),
    re_path(
        r"^browse/",
        never_cache(views.browse),
        name="ckeditor_browse",
    ),
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n', include('django.conf.urls.i18n')),
    path('api/v1/', include(api_urlpatterns)),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ckeditor/', include(ckeditor_urls)),
]
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns


urlpatterns += i18n_patterns(
    path('blog/', include('apps.blog.urls')),
    path('', RedirectView.as_view(url='blog/', permanent=True)),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('<slug:slug>/', TextPageView.as_view(), name='textpage'),
)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
