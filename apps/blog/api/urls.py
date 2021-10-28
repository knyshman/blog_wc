from django.urls import path
from .views import ArticleView, SingleArticleView, ArticleCreateView, ArticleUpdateAPIView, ProfileView, LikeCreate

app_name = "articles"

urlpatterns = [
    path('create/', ArticleCreateView.as_view()),
    path('<slug:slug>/', SingleArticleView.as_view()),
    path('<slug:slug>/update', ArticleUpdateAPIView.as_view()),
    path('', ArticleView.as_view()),

    path('like/', LikeCreate.as_view()),
    path('profile/', ProfileView.as_view())
]