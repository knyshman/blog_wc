"""blog_wc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from apps.accounts.views import PasswordChange
from apps.blog.views import ProfileDetailView, ProfileUpdateView, MyUserFavouriteArticles

User = get_user_model()

api_urlpatterns = [
    path('blog/', include('apps.blog.api.urls')),
    # path('accounts/', include('apps.accounts.api.urls'))

]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n', include('django.conf.urls.i18n')),
    path('api/v1/', include(api_urlpatterns)),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),


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

urlpatterns += i18n_patterns(
    path('blog/', include('apps.blog.urls')),
    path('', RedirectView.as_view(url='blog/', permanent=True)),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('ckeditor/', include(ckeditor_urls)),
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('profile/password_change/', PasswordChange.as_view(), name='password_change'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/favourite_articles/', MyUserFavouriteArticles.as_view(), name='favourite_articles'),
)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

