from django.urls import path
from .views import ArticleDetailView, ArticleListView, ArticleUpdateView, \
    ArticleCreateView, ArticleDeleteView, CommentCreateView, RatingCreateView, LikeCreateView,\
    Subscribes


urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('create/', ArticleCreateView.as_view(), name='article_create'),
    path('<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<slug:slug>/update/', ArticleUpdateView.as_view(), name='article_update'),
    path('<slug:slug>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('<slug:slug>/comment', CommentCreateView.as_view(), name='comment_create'),
    path('<slug:slug>/rating', RatingCreateView.as_view(), name='rating'),
    path('<slug:slug>/like', LikeCreateView.as_view(), name='like'),
    path('<slug:slug>/subscribes/<int:pk>', Subscribes.as_view(), name='subscribes')

]
