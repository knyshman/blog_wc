from django.urls import path, include
from .views import ArticleView, SingleArticleView, ArticleCreateView, ArticleUpdateAPIView, ProfileView, LikeCreate, SubscribeView, ImageCreateApiView

app_name = "articles"


slug_url_patterns = [
    path('', SingleArticleView.as_view(), name='article_api_detail'),
    path('update/', ArticleUpdateAPIView.as_view(), name='article_api_update'),
    path('like/', LikeCreate.as_view(), name='like_api'),
    path('subscribes/', SubscribeView.as_view(), name='subscribes_api'),
    path('image/', ImageCreateApiView.as_view())
]

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='article_api_create'),
    path('', ArticleView.as_view(), name='article_api_list'),
    path('profile/', ProfileView.as_view(), name='api_profile'),
    path('<slug:slug>/', include(slug_url_patterns))
]