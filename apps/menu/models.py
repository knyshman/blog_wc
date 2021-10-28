from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Menu(models.Model):
    name = models.CharField(verbose_name=_('Название'), max_length=50)
    url = models.URLField(verbose_name=_('Ссылка'), max_length=100)
    target = models.SmallIntegerField(choices=[(0, '_self'), (1, '_blank')], default=0)
    position = models.SmallIntegerField(verbose_name=_('Позиция'), choices=[(0, 'Header'), (1, 'Footer')], default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Элемент меню')
        verbose_name_plural = _('Элементы меню')

    def __str__(self):
        return str(self.name)


class TextPage(models.Model):
    name = models.CharField(verbose_name=_('Название'), max_length=50)
    content = RichTextUploadingField(verbose_name=_('Контент'))
    url = models.CharField(verbose_name=_('Ссылка'), max_length=100)
    target = models.SmallIntegerField(choices=[(0, '_self'), (1, '_blank')], default=0)
    position = models.SmallIntegerField(verbose_name=_('Позиция'), choices=[(0, 'Header'), (1, 'Footer')], default=0)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
