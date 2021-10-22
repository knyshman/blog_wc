from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView
from ..models import Article
from .serializers import ArticleSerializer


class ArticleView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SingleArticleView(RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer