from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from modeltranslation.forms import forms
from ckeditor.fields import RichTextFormField
from .models import Author, SemiCategory, Article, Category, Comment
from ..accounts.models import MyUser

User = get_user_model()


class ArticleForm(forms.ModelForm):
    title = forms.CharField(label=_('Заголовок'), widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('Введите заголовок')
    }))
    content = RichTextFormField(label=_('Введите текст'))
    author = forms.ModelChoiceField(
        label=_('Автор'),
        queryset=Author.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}
    ))
    category = forms.ModelChoiceField(label=_('Категория'), queryset=SemiCategory.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Article
        fields = ('category', 'author', 'title', 'content', 'preview_image')


class ArticleFilterForm(forms.Form):
    author = forms.ModelChoiceField(
        label='Автор', queryset=Author.objects.all(), widget=forms.Select(
            attrs={'class': 'form-control js-example-basic-single'}
        )
    )
    category = forms.ModelChoiceField(
        label='Категория', queryset=Category.objects.all(), widget=forms.Select(
            attrs={'class': 'form-control js-example-basic-single'}
        )
    )
    semi_category = forms.ModelMultipleChoiceField(
        label='Подкатегории', queryset=SemiCategory.objects.all(),
        required=False, widget=forms.SelectMultiple(
            attrs={'class': 'form-control js-example-basic-multiple'}
        )
    )
    #
    #
    #     label=_('Автор'),
    #     queryset=MyUser.objects.all(),
    #     widget=forms.Select(attrs={'class': 'form-control'}
    # )

class CommentForm(forms.ModelForm):
    comment = RichTextFormField(label=_('Введите текст'))
    article = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=Article.objects.all())

    class Meta:
        model = Comment
        fields = ('comment', 'rating', 'article')