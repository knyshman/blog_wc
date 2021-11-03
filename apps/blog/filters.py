import django_filters
from django.utils.translation import ugettext_lazy as _
from .models import Article, Category


class ArticleFilter(django_filters.FilterSet):
    """Фильтр по категориям, автору. Поиск по названию, сортировка по дате и рейтингу"""
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label=_('Название'))
    category = django_filters.ModelChoiceFilter(lookup_expr='exact', queryset=Category.objects.all(), method='get_relative_categories')
    o = django_filters.OrderingFilter(
        label=_('Cортировать'),
        fields=(
            ('create_date', 'create_date'),
            ('average_rating', 'average_rating'),

        ),
        field_labels={
            'create_date': _('по дате'),
            '-create_date': _('по дате \u25BC'),
            'average_rating': _('по рейтингу'),
            '-average_rating': _('по рейтингу \u25BC'),
    }
    )

    class Meta:
        model = Article
        fields = {
            'author': ['exact'],
            'category': ['exact']
        }

    @staticmethod
    def get_relative_categories(queryset, category, value):
        """Получаем родительские категории"""
        categories = list(value.get_descendants()) + [value]
        qs = queryset.filter(category__in=categories)
        return qs

