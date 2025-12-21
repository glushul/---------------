from rest_framework import serializers
from .models import Company, Vacancy, FieldOfStudy
from . import models

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class VacancySerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        write_only=True,
        source='company'
    )

    class Meta:
        model = Vacancy
        fields = '__all__'

    def validate(self, data):
        salary_min = data.get('salary_min')
        salary_max = data.get('salary_max')

        if salary_min is not None and salary_max is not None:
            if salary_min > salary_max:
                raise serializers.ValidationError({
                    'salary_min': 'Минимальная зарплата не может быть больше максимальной.',
                    'salary_max': 'Максимальная зарплата не может быть меньше минимальной.'
                })
        elif salary_min is not None and salary_max is None:
            pass
        elif salary_max is not None and salary_min is None:
            pass

        employment_type = data.get('employment_type')
        if employment_type:
            valid_types = [choice[0] for choice in models.EMPLOYMENT_TYPE_CHOICES]
            if employment_type not in valid_types:
                raise serializers.ValidationError({
                    'employment_type': f'Недопустимое значение. Допустимые: {", ".join(valid_types)}'
                })

        experience = data.get('experience')
        if experience:
            valid_experiences = [choice[0] for choice in models.EXPERIENCE_CHOICES]
            if experience not in valid_experiences:
                raise serializers.ValidationError({
                    'schedule': f'Недопустимое значение. Допустимые: {", ".join(valid_experiences)}'
                })
            
        schedule = data.get('schedule')
        if schedule:
            valid_schedules = [choice[0] for choice in models.SCHEDULE_CHOICES]
            if schedule not in valid_schedules:
                raise serializers.ValidationError({
                    'schedule': f'Недопустимое значение. Допустимые: {", ".join(valid_schedules)}'
                })

        return data

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Название вакансии не может быть пустым.")
        if len(value) > 255:
            raise serializers.ValidationError("Название не должно превышать 255 символов.")
        return value.strip()

    def validate_city(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Город не может состоять только из пробелов.")
        return value.strip() if value else value

    def validate_requirements(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Поле 'требования' не может быть пустым.")
        return value

    def validate_responsibilities(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Поле 'обязанности' не может быть пустым.")
        return value

    def validate_conditions(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Поле 'условаия' не может быть пустым.")
        return value
    
class FieldOfStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOfStudy
        fields = '__all__'