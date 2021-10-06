import django_filters
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .models import Article


class ArticleFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label=_('Название'))

    o = django_filters.OrderingFilter(
        label=_('Cортировать'),
        fields=(
            ('title', 'title'),
            ('average_rating', 'average_rating'),

        ),
        field_labels={
            'title': _('по названию'),
            'average_rating': _('по рейтингу')
    }
    )

    class Meta:
        model = Article
        fields = {
            'author': ['exact'],
            'category': ['exact']
        }
