from modeltranslation.translator import register, TranslationOptions
from .models import MyUser


@register(MyUser)
class MyUserTranslationOptions(TranslationOptions):
    fields = ('name', 'last_name', )