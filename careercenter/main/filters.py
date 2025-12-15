import django_filters
from .models import Vacancy

class VacancyFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name="is_active")

    company__industry = django_filters.CharFilter(lookup_expr='icontains')

    salary_min = django_filters.NumberFilter(field_name='salary_min', lookup_expr='gte')

    title = django_filters.CharFilter(lookup_expr='icontains')

    city = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Vacancy
        fields = ['is_active']