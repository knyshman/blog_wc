from django.urls import path, include
from .views import ArticleDetailView, ArticleListView, ArticleUpdateView, \
    ArticleCreateView, ArticleDeleteView, CommentCreateView, RatingCreateView, LikeCreateView,\
    Subscribes

slug_url_patterns = [
    path('', ArticleDetailView.as_view(), name='article_detail'),
    path('update/', ArticleUpdateView.as_view(), name='article_update'),
    path('delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('comment', CommentCreateView.as_view(), name='comment_create'),
    path('rating', RatingCreateView.as_view(), name='rating'),
    path('like', LikeCreateView.as_view(), name='like'),
    path('subscribes/', Subscribes.as_view(), name='subscribes')
]

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('create/', ArticleCreateView.as_view(), name='article_create'),
    path('<slug:slug>/', include(slug_url_patterns)),


]
