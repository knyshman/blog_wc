from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, CreateAPIView, RetrieveAPIView
from .permissions import OwnPermission
from ..models import Article
from .serializers import ArticleSerializer, ArticlePostSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import ugettext_lazy as _


class ArticleView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    verbose_name = _('Блог')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ArticleCreateView(CreateAPIView):
    serializer_class = ArticlePostSerializer
    permission_classes = [IsAuthenticated]
    verbose_name = _('Новая статья')

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticlePostSerializer
    permission_classes = (IsAuthenticated, OwnPermission,)
    verbose_name = _('Изменение статьи')


class SingleArticleView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
