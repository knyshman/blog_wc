from django.core.exceptions import ValidationError
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Avg
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _
from django.db import models
from ckeditor.fields import RichTextField
from treebeard.mp_tree import MP_Node
from ..accounts.models import MyUser


class Category(MP_Node):
    name = models.CharField(verbose_name=_('Категория'), max_length=200, unique=True)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.name

#
# class Author(models.Model):
#     user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100, verbose_name=_('Название'), unique=True)
#
#     class Meta:
#         verbose_name = 'Автор'
#         verbose_name_plural = 'Авторы'
#
#     def __str__(self):
#         return self.name


class Article(models.Model):
    category = models.ForeignKey(Category, verbose_name=_('Категория'), on_delete=models.SET_NULL, null=True, related_name='category')
    title = models.CharField(max_length=250, verbose_name=_('Название'), unique=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    content = RichTextField(verbose_name=_('Описание'), null=True, blank=True)
    short_description = models.CharField(verbose_name=_('Краткое описание'), max_length=300, blank=True)
    images = RichTextUploadingField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(MyUser, verbose_name=_('Автор'), on_delete=models.SET_NULL, null=True, related_name='article_author')
    average_rating = models.FloatField(null=True, blank=True, default=0)

    class Meta:
        verbose_name = _('Статья')
        verbose_name_plural = _('Статьи')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.short_description:
            self.short_description = self.content
        if not self.slug:
            self.slug = slugify(str(self.title).replace(' ', '-'))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    author = models.ForeignKey(MyUser, max_length=200, on_delete=models.SET_NULL, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    comment = RichTextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comment_set', related_query_name='comments_set')
    is_published = models.BooleanField(null=True, default=True)


class ArticleRating(models.Model):
    rating = models.IntegerField(verbose_name=_('Рейтинг'), default=0)
    user = models.CharField(max_length=200)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='rating_set')

    def __str__(self):
        return str(self.rating)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.article.average_rating = round((self.article.rating_set.aggregate(avg_rating=Avg('rating'))['avg_rating']), 2)
    #     self.article.save()