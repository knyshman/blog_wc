from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.db import models
from ckeditor.fields import RichTextField
from .utils import from_cyrillic_to_eng

User = get_user_model()


class Category(models.Model):
    name = models.CharField(verbose_name=_('Категория'), max_length=200)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class SemiCategory(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250, verbose_name='название')

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.name


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='название', unique=True)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.name


class Article(models.Model):
    category = models.ForeignKey(SemiCategory, verbose_name='Категория', on_delete=models.SET_NULL, null=True, related_name='semi_category')
    title = models.CharField(max_length=250, verbose_name='Название', unique=True)
    slug = models.SlugField(blank=True, unique=True)
    content = RichTextField(verbose_name='Описание', null=True, blank=True)
    short_description = models.CharField(verbose_name='Краткое описание', max_length=300, blank=True)
    image = models.ImageField(blank=True)
    update_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, verbose_name='Автор', on_delete=models.SET_NULL, null=True)
    rating_choices = [
    ('1', 'very bad'),
    ('2', 'bad'),
    ('3', 'good'),
    ('4', 'very good'),
    ('5', 'excellent'),
]
    rating = models.CharField(verbose_name='Рейтинг', max_length=10, choices=rating_choices)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.title))
        if not self.short_description:
            self.short_description = self.content
        super().save(*args, **kwargs)
