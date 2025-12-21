from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views, api

router = DefaultRouter()
router.register(r'companies', api.CompanyViewSet)
router.register(r'vacancies', api.VacancyViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path("", views.main, name="main"),
    path("vacancies", views.get_vacancies, name="vacancies"),
    path("vacancies/<int:id>", views.get_vacancy, name="get_vacancy"),
    path('vacancies/<str:id>/edit/', views.edit_vacancy, name="edit_vacancy"),
    path("companies", views.get_companies, name="companies"),
    path("companies/<str:id>/edit/", views.edit_company, name="edit_company"),
    path('export/vacancies/company/<int:company_id>/', views.export_vacancies_xlsx, name='export_vacancies')
]