from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from django_starfield import Stars
from modeltranslation.forms import forms
from ckeditor.fields import RichTextFormField
from .models import Article, Category, Comment, ArticleRating, Like, Image


User = get_user_model()


class ArticleForm(forms.ModelForm):
    title = forms.CharField(label=_('Заголовок'), widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('Введите заголовок')
    }))
    author = forms.ModelChoiceField(
        label=_('Автор'),
        queryset=User.objects.all(),
        widget=forms.HiddenInput(),
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


ArticleFormSet = inlineformset_factory(Article, Image, fields='__all__', can_delete=True)


class CommentForm(forms.ModelForm):
    comment = RichTextFormField(label=_('Ваш комментарий'))
    article = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=Article.objects.all())
    author = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=User.objects.all())

    class Meta:
        model = Comment
        fields = ('comment', 'article', 'author')


class RatingForm(forms.ModelForm):
    rating = forms.IntegerField(widget=Stars, label=_('Ваша оценка'))
    user = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=User.objects.all())
    article = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=Article.objects.all())

    class Meta:
        model = ArticleRating
        fields = ('rating', 'article', 'user')


class LikeForm(forms.ModelForm):
    like = forms.BooleanField(label='Like', widget=forms.HiddenInput)
    user = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=User.objects.all())
    article = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=Article.objects.all())

    class Meta:
        model = Like
        fields = ('like', 'article', 'user')


class ProfileForm(forms.ModelForm):

    name = forms.CharField(label=_('Имя'), widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('Введите имя')
    }))
    last_name = forms.CharField(label=_('Фамилия'), widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': _('Введите фамилию')
    }))
    phone = forms.CharField(label=_('Телефон'), validators=['only_int'], widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': _('Введите номер телефона')
    }))
    avatar = forms.ImageField(label=_('Фото'))

    class Meta:
        model = User
        fields = ('name', 'last_name', 'phone', 'avatar')

    def only_int(value):
        if not value.isdigit():
            raise ValidationError(_('Номер телефона должен содержать только цифры(не более 10)'))





