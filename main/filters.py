import django_filters

from .models import Vacancy


class VacancyFilter(django_filters.FilterSet):
    salary_min = django_filters.NumberFilter(field_name="salary_min", lookup_expr="gte")

    title = django_filters.CharFilter(lookup_expr="icontains")

    city = django_filters.CharFilter(lookup_expr="iexact")

    class Meta:
        model = Vacancy
        fields = []
