from modeltranslation.translator import register, TranslationOptions
from .models import Menu, TextPage


@register(Menu)
class MenuTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(TextPage)
class TextPageTranslationOptions(TranslationOptions):
    fields = ('name', 'content' )