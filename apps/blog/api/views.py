from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, CreateAPIView, \
    RetrieveDestroyAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.views import APIView

from .paginations import CustomPagination
from .permissions import OwnPermission
from ..filters import ArticleFilter
from ..models import Article, Like
from .serializers import ArticleSerializer, ArticlePostSerializer, ProfileSerializer, LikeSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import ugettext_lazy as _
from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.renderers import BrowsableAPIRenderer, AdminRenderer, JSONRenderer
# from .renderers import CustomRenderer, ApiRenderer
User = get_user_model()


class ArticleView(ListAPIView):
    lookup_field = 'slug'
    queryset = Article.objects.all().prefetch_related('image_set')
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArticleFilter
    pagination_class = CustomPagination


class ArticleCreateView(CreateAPIView):
    serializer_class = ArticlePostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleUpdateAPIView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Article.objects.prefetch_related('image_set').all()
    serializer_class = ArticlePostSerializer
    permission_classes = (IsAuthenticated, OwnPermission,)
    verbose_name = _('Изменение статьи')


class LikeCreate(CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.select_related('user', 'article').all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, like=True)


class SingleArticleView(RetrieveAPIView):
    lookup_field = 'slug'
    queryset = Article.objects.prefetch_related('image_set').all()
    serializer_class = ArticleSerializer


# class SubscribeView(RetrieveAPIView):
#     lookup_field = 'slug'
#     queryset = Article.objects.prefetch_related('image_set').all()
#     serializer_class = ArticleSerializer
#
#     def post(self, request, *args, **kwargs):
#         print(self.kwargs)
#         article = Article.objects.select_related('author', 'category').filter(slug=self.kwargs['slug']).first()
#         author = article.author
#         current_user = self.get_object()
#         print(current_user.subscribes)
#         if current_user != author:
#             if current_user.subscribes.filter(id=author.id).exists():
#                 current_user.subscribes.remove(author)
#             else:
#                 current_user.subscribes.add(author)


class ProfileView(RetrieveUpdateAPIView):
    lookup_field = None
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        return queryset
