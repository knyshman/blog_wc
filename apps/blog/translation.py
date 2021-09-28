from modeltranslation.translator import register, TranslationOptions
from .models import Author, Article, Category, SemiCategory


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('category', 'title', 'content', 'short_description', 'author')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(SemiCategory)
class SemiCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'category')

