from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Article, Author, Category, SemiCategory, ArticleImage, Comment


class ArticleAdminForm(forms.ModelForm):
    description_ru = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    description_ua = forms.CharField(label='Опис', widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label='Description', widget=CKEditorUploadingWidget())

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
class CategoryAdmin(TranslationAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


@admin.register(SemiCategory)
class SemiCategoryAdmin(TranslationAdmin):
    list_display = ('name', )
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Author)
class AuthorAdmin(TranslationAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    list_display = ('category', 'title', 'content', 'short_description', 'author')
    list_display_links = ('category', 'title', 'content', 'short_description', 'author')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(ArticleImage)
admin.site.register(Comment)