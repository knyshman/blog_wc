from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from modeltranslation.admin import forms, TranslationAdmin, TabbedTranslationAdmin
from .models import Menu, TextPage


class TextPageAdminForm(forms.ModelForm):
    content_ru = forms.CharField(label='Контент', widget=CKEditorUploadingWidget())
    content_ua = forms.CharField(label='Контент', widget=CKEditorUploadingWidget())
    content_en = forms.CharField(label='Content', widget=CKEditorUploadingWidget())

    class Meta:
        model = TextPage
        fields = '__all__'


class MenuAdmin(SortableAdminMixin, TabbedTranslationAdmin):
    list_display = ('id', 'name' )
    list_display_links = ('name', )


class TextPageAdmin(TranslationAdmin):
    list_display = ('name', 'content')
    list_display_links = ('name', 'content')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Menu, MenuAdmin)
admin.site.register(TextPage, TextPageAdmin)