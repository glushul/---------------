from . import models, serializers, pagination, filters

from rest_framework import viewsets, filters as rest_framework_filters
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
    pagination_class = pagination.StandardResultsSetPagination

class VacancyViewSet(viewsets.ModelViewSet):
    queryset = models.Vacancy.objects.all()
    serializer_class = serializers.VacancySerializer
    pagination_class = pagination.StandardResultsSetPagination
    filterset_class = filters.VacancyFilter
    filter_backends = [
        DjangoFilterBackend,
        rest_framework_filters.SearchFilter,
        rest_framework_filters.OrderingFilter  
    ]
    search_fields = ['title', 'description', 'company__name']
    ordering_fields = ['salary_max', 'salary_min']

    def get_queryset(self):
        qs = models.Vacancy.objects.all()
        if self.request.query_params.get('my') == 'true':
            if self.request.user.is_authenticated and hasattr(self.request.user, 'company'):
                qs = qs.filter(company=self.request.user.company)
            else:
                return qs.none()

        active_param = self.request.query_params.get('is_active')
        if active_param is not None:
            qs = qs.filter(is_active=(active_param.lower() == 'true'))

        return qs
    
    @action(detail=False, methods=['GET'], url_path='active')
    def active(self, request):
        active_vacancies = self.get_queryset().filter(is_active=True)
        page = self.paginate_queryset(active_vacancies)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(active_vacancies, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST'], url_path='archive')
    def archive(self, request, pk=None):
        vacancy = self.get_object()
        vacancy.is_active = False
        vacancy.save(update_fields=['is_active'])
        serializer = self.get_serializer(vacancy)
        return Response(serializer.data, status=status.HTTP_200_OK)
