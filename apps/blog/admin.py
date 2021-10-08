from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Article, Category, Comment, ArticleRating
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


class ArticleAdminForm(forms.ModelForm):
    content_ru = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    content_ua = forms.CharField(label='Опис', widget=CKEditorUploadingWidget())
    content_en = forms.CharField(label='Description', widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = '__all__'


class CommentAdminForm(forms.ModelForm):
    comment_ru = forms.CharField(label='Комментарий', widget=CKEditorUploadingWidget())
    comment_ua = forms.CharField(label='Коментар', widget=CKEditorUploadingWidget())
    comment_en = forms.CharField(label='Comment', widget=CKEditorUploadingWidget())

    class Meta:
        model = Comment
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(TranslationAdmin, TreeAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    form = movenodeform_factory(Category)


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    list_display = ('category', 'title', 'content', 'short_description', 'author')
    list_display_links = ('category', 'title', 'content', 'short_description', 'author')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Comment)
admin.site.register(ArticleRating)
