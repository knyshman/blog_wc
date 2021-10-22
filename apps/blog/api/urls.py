from django.urls import path
from .views import ArticleView, SingleArticleView

app_name = "articles"

urlpatterns = [
    path('<int:pk>/', SingleArticleView.as_view()),
    path('', ArticleView.as_view()),


]