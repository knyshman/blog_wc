from django.urls import path
from .views import ArticleView, SingleArticleView, ArticleCreateView, ArticleUpdateAPIView

app_name = "articles"

urlpatterns = [
    path('<int:pk>/', SingleArticleView.as_view()),
    path('<int:pk>/update', ArticleUpdateAPIView.as_view()),
    path('', ArticleView.as_view()),
    path('create/', ArticleCreateView.as_view())


]