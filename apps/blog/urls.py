from django.urls import path
from .views import ArticleDetailView, ArticleListView, ArticleUpdateView, ArticleCreateView, ArticleDeleteView

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('detail/<str:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<str:slug>/update/', ArticleUpdateView.as_view(), name='article_update'),
    path('create/', ArticleCreateView.as_view(), name='article_create'),
    path('<str:slug>/delete/', ArticleDeleteView.as_view(), name='article_delete'),



]