from import_export import resources
from import_export.fields import Field
from .models import Vacancy
from . import models

class VacancyResource(resources.ModelResource):
    title = Field(attribute='title', column_name='Название')
    company_name = Field(attribute='company__name', column_name='Компания')
    industry = Field(attribute='company__industry', column_name='Индустрия')
    city = Field(attribute='city', column_name='Город')
    address = Field(attribute='address', column_name='Адрес')
    employment_type = Field(attribute='employment_type', column_name='Тип трудоустройства')
    experience = Field(attribute='experience', column_name='Опыт работы')
    schedule = Field(attribute='schedule', column_name='График работы')
    salary_min = Field(attribute='salary_min', column_name='Мин. зарплата')
    salary_max= Field(attribute='salary_max', column_name='Макс. зарплата')
    created_at = Field(attribute='created_at', column_name='Создана')

    def dehydrate_employment_type(self, vacancy):
        return dict(models.EMPLOYMENT_TYPE_CHOICES).get(vacancy.employment_type, vacancy.employment_type)

    def dehydrate_experience(self, vacancy):
        return dict(models.EXPERIENCE_CHOICES).get(vacancy.experience, vacancy.experience)

    def dehydrate_schedule(self, vacancy):
        return dict(models.SCHEDULE_CHOICES).get(vacancy.schedule, vacancy.schedule)

    class Meta:
        model = Vacancy
        fields = (
            'id',
            'title',
            'company_name',
            'industry',
            'city',
            'address',
            'employment_type',
            'experience',
            'schedule',
            'salary_min',
            'salary_max',
            'created_at',
        )
        export_order = fields