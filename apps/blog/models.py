from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.db import models
from ckeditor.fields import RichTextField
from treebeard.mp_tree import MP_Node
from .utils import from_cyrillic_to_eng


User = get_user_model()


class Category(MP_Node):
    """Модель категорий статей"""
    name = models.CharField(verbose_name=_('Категория'), max_length=200, unique=True, db_index=True)
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(from_cyrillic_to_eng(str(self.name)))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    """Модель статьи"""
    category = models.ForeignKey(Category, verbose_name=_('Категория'), on_delete=models.SET_NULL, null=True, related_name='category')
    title = models.CharField(max_length=250, verbose_name=_('Название'), unique=True, db_index=True)
    slug = models.SlugField(max_length=250, blank=True, null=True, unique=True)
    preview_image = models.ImageField(verbose_name=_('Изображение превью'), blank=True, default='default.jpg')
    short_description = models.TextField(verbose_name=_('Краткое описание'), max_length=300, blank=True)
    content = RichTextUploadingField(verbose_name=_('Контент'))
    create_date = models.DateTimeField(verbose_name=_('Дата создания'), auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=_('Дата изменения'), auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_('Автор'))
    average_rating = models.FloatField(verbose_name=_('Средний рейтинг'), default=0)
    likes = models.IntegerField(verbose_name=_('Лайки'), default=0)
    is_recommended = models.BooleanField(verbose_name=_('Рекомендуемая'), default=False)

    class Meta:
        verbose_name = _('Статья')
        verbose_name_plural = _('Статьи')
        ordering = ['id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.short_description:
            self.short_description = self.content
        if not self.slug:
            self.slug = slugify(from_cyrillic_to_eng(str(self.title)))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})


class Image(models.Model):
    """Модель изображений в статье"""
    article = models.ForeignKey(Article, verbose_name=_('статья'), on_delete=models.CASCADE)
    image = models.ImageField(verbose_name=_('изображение'), upload_to='media')
    alt = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = _('Изображение')
        verbose_name_plural = _('Изображения')
        ordering = ['alt']

    def save(self, *args, **kwargs):
        if not self.alt:
            self.alt = f'{self.article.slug}{self.pk}'
        super().save()


class Comment(models.Model):
    """Модель комментария"""
    author = models.ForeignKey(User, verbose_name=_('пользователь'),  on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name=_('дата создания'), auto_now_add=True)
    comment = RichTextField(verbose_name=_('Комментарий'), config_name='awesome_ckeditor')
    article = models.ForeignKey(Article, verbose_name=_('Статья'), on_delete=models.CASCADE, related_name='comment_set', related_query_name='comments_set')
    is_published = models.BooleanField(verbose_name=_('опубликовано'), null=True, default=True)

    class Meta:
        verbose_name = _('Комментарий')
        verbose_name_plural = _('Комментарии')
        ordering = ['create_date']


class ArticleRating(models.Model):
    """Модель рейтинга статьи"""
    rating = models.IntegerField(verbose_name=_('Рейтинг'), default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='rating_set')

    def __str__(self):
        return str(self.rating)


class Like(models.Model):
    """Модель лайка, добавляет(удаляет) статью в избранное"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_query_name='articles')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=True)
