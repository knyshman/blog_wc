from django.urls import path, include
from . import views
from ..accounts.views import PasswordChange

slug_url_patterns = [
    path('', views.ArticleDetailView.as_view(), name='article_detail'),
    path('update/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('comment', views.CommentCreateView.as_view(), name='comment_create'),
    path('rating', views.RatingCreateView.as_view(), name='rating'),
    path('like', views.LikeCreateView.as_view(), name='like'),
    path('subscribes/', views.Subscribes.as_view(), name='subscribes')
]
profile_urls = [
    path('', views.ProfileDetailView.as_view(), name='profile'),
    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path('update/', views.ProfileUpdateView.as_view(), name='profile_update'),

]
urlpatterns = [
    path('', views.ArticleListView.as_view(), name='home'),
    path('profile/', include(profile_urls)),
    path('favourite_articles/', views.MyUserFavouriteArticles.as_view(), name='favourite_articles'),
    path('create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('<slug:slug>/', include(slug_url_patterns)),
]
