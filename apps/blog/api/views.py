from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, CreateAPIView, \
    RetrieveAPIView, RetrieveUpdateDestroyAPIView
from .paginations import CustomPagination
from .permissions import OwnPermission
from ..filters import ArticleFilter
from ..models import Article, Like, Image
from .serializers import ArticleSerializer, ArticlePostSerializer, ProfileSerializer, LikeSerializer, \
    SubscribesSerializer, ImagePostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer
from django.utils.translation import ugettext_lazy as _
from .renderers import CustomRenderer
User = get_user_model()


class ArticleView(ListAPIView):
    queryset = Article.objects.all().prefetch_related('image_set')
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArticleFilter
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    pagination_class = CustomPagination


class ArticleCreateView(CreateAPIView):
    serializer_class = ArticlePostSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleUpdateAPIView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Article.objects.prefetch_related('image_set').all()
    serializer_class = ArticlePostSerializer
    permission_classes = (IsAuthenticated, OwnPermission,)
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    verbose_name = _('Изменение статьи')


class LikeCreate(CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.select_related('user', 'article').all()
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        article = Article.objects.select_related('category', 'author').filter(slug=self.kwargs['slug']).first()
        serializer.save(user=self.request.user, like=True, article=article)


class SingleArticleView(RetrieveAPIView):
    lookup_field = 'slug'
    queryset = Article.objects.prefetch_related('image_set').all()
    serializer_class = ArticleSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class SubscribeView(RetrieveUpdateAPIView):
    lookup_field = None
    queryset = User.objects.all()
    serializer_class = SubscribesSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def get_object(self):
        article = Article.objects.select_related('author', 'category').filter(slug=self.kwargs['slug']).first()
        author = article.author
        return author

    def put(self, request, *args, **kwargs):
        article = Article.objects.select_related('author', 'category').filter(slug=self.kwargs['slug']).first()
        author = article.author
        current_user = self.request.user
        if current_user != author:
            if author.subscribes.filter(id=current_user.id).exists():
                author.subscribes.remove(current_user)
            else:
                author.subscribes.add(current_user)
        return self.update(request, *args, **kwargs)


class ProfileView(RetrieveUpdateAPIView):
    lookup_field = None
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        queryset = User.objects.filter(id=self.request.user.id)
        return queryset


class ImageCreateApiView(CreateAPIView):
    serializer_class = ImagePostSerializer
    queryset = Image.objects.all()
    permission_classes = (IsAuthenticated, )
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def perform_create(self, serializer):
        article = Article.objects.select_related('category', 'author').filter(slug=self.kwargs['slug']).first()
        if article.author == self.request.user:
            serializer.save(article=article)
        else:
            raise ValidationError(_('Вы не можете добавлять изображения к этой статье!!!'))