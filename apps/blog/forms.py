from django.utils.translation import ugettext_lazy as _
from modeltranslation.forms import forms
from ckeditor.fields import RichTextFormField
from .models import Author, SemiCategory, Article


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
