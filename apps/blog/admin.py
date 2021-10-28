from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminMixin
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, forms, TabbedTranslationAdmin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Article, Category, Comment, ArticleRating, Like, Image
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from django.utils.translation import ugettext_lazy as _


class ImageAdmin(SortableInlineAdminMixin, admin.StackedInline):
    model = Image
    list_display = ('image', 'alt')
    list_display_links = ('image', 'alt')


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
class CategoryAdmin(TabbedTranslationAdmin, TreeAdmin):
    list_display = ('name',)
    search_fields = ('name', )
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    form = movenodeform_factory(Category)


@admin.register(Article)
class ArticleAdmin(SortableAdminMixin, TabbedTranslationAdmin):
    sortable_by = ['title', 'average_rating', 'likes', 'author', 'create_date']
    list_display = ('category', 'title', 'author', 'create_date', 'update_date', 'likes', 'average_rating', 'is_recommended')
    list_display_links = ('author', 'title')
    list_editable = ('is_recommended',)
    list_per_page = 30
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    list_select_related = ('category', 'author')
    readonly_fields = ('create_date', 'update_date', 'likes', 'average_rating')
    inlines = [ImageAdmin]
    save_on_top = True
    actions = ('set_recommended', 'set_unrecommended')

    def set_recommended(self, request, queryset):
        for article in queryset:
            article.is_recommended = True
            article.save()

    def set_unrecommended(self, request, queryset):
        for article in queryset:
            article.is_recommended = False
            article.save()

    set_recommended.short_description = _('Добавить в рекомендуемые')
    set_recommended.short_description = _('Убрать из рекомендуемых')


@admin.register(Comment)
class CommentAdmin(SortableAdminMixin, TabbedTranslationAdmin):
    list_display = ('author', 'create_date', 'is_published', 'article', 'comment')
    list_editable = ('is_published', )
    list_select_related = ('article', 'author')
    readonly_fields = ('create_date', 'comment', 'author')
    list_filter = ['is_published']
    save_on_top = True
    actions = ('set_unpublished',)

    def set_unpublished(self, request, queryset):
        for comment in queryset:
            comment.is_published = False
            comment.save()

    set_unpublished.short_description = _('Сделать неопубликованными')


admin.site.register(Image)
