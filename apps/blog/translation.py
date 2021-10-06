from modeltranslation.translator import register, TranslationOptions
from .models import Article, Category


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('category', 'title', 'content', 'short_description', 'author')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)



