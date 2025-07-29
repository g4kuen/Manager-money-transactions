import django_filters
from .models import Record


class RecordFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name='date', label='Диапазон дат')

    class Meta:
        model = Record
        fields = ['status', 'type', 'category', 'subcategory']