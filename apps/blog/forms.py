from django.utils.translation import ugettext_lazy as _
from django_starfield import Stars
from modeltranslation.forms import forms
from ckeditor.fields import RichTextFormField
from .models import Article, Category, Comment, ArticleRating, Like
from ..accounts.models import MyUser


class ArticleForm(forms.ModelForm):
    title = forms.CharField(label=_('Заголовок'), widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('Введите заголовок')
    }))
    author = forms.ModelChoiceField(
        label=_('Автор'),
        queryset=MyUser.objects.all(),
        widget=forms.HiddenInput(),
        required=False
    )
    category = forms.ModelChoiceField(label=_('Категория'), queryset=Category.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    slug = forms.SlugField(required=False)

    class Meta:
        model = Article
        fields = ('category', 'author', 'title', 'short_description', 'content', 'slug', 'preview_image' )

    def get_author(self):
        self.author = self.request.user
        return self.author


class CommentForm(forms.ModelForm):
    comment = RichTextFormField(label=_('Комментарий'))
    article = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=Article.objects.all())
    author = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=MyUser.objects.all())

    class Meta:
        model = Comment
        fields = ('comment', 'article', 'author')


class RatingForm(forms.ModelForm):
    rating = forms.IntegerField(widget=Stars, label='Оценка')
    user = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=MyUser.objects.all())
    article = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=Article.objects.all())

    class Meta:
        model = ArticleRating
        fields = ('rating', 'article', 'user')


class LikeForm(forms.ModelForm):
    like = forms.BooleanField(label='Like', widget=forms.HiddenInput)
    user = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=MyUser.objects.all())
    article = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=Article.objects.all())

    class Meta:
        model = Like
        fields = ('like', 'article', 'user')