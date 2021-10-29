from modeltranslation.translator import register, TranslationOptions
from .models import Article, Category, Comment


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('category', 'title', 'content', 'short_description')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Comment)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('comment',)

