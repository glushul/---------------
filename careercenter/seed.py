# seed.py
import os
import sys

# Добавляем корень проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Указываем Django, где находятся настройки
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careercenter.settings")

# Инициализируем Django
import django
django.setup()

# Только ПОСЛЕ этого можно импортировать модели!
from main.models import (
    User, Company, FieldOfStudy, Vacancy
)
from faker import Faker
from random import choice, sample

fake = Faker('ru_RU')

def seed_data():
    from django.db import transaction
    with transaction.atomic():
        print("🗑️ Удаление старых данных...")
        Vacancy.objects.all().delete()
        Company.objects.all().delete()
        FieldOfStudy.objects.all().delete()
        User.objects.all().delete()

        print("👤 Создание пользователей...")
        users = []
        for _ in range(15):
            user = User.objects.create(
                email=fake.unique.email(),
                full_name=fake.name(),
                role='student'
            )
            users.append(user)

        partner = User.objects.create(email='hr@company.ru', full_name='HR Партнёр', role='partner')

        print("📚 Создание направлений подготовки...")
        field_names = ['Информационные технологии', 'Экономика', 'Машиностроение', 'Управление', 'Дизайн', 'Робототехника']
        fields = [FieldOfStudy.objects.create(name=name) for name in field_names]

        print("🏢 Создание компаний...")
        company_names = ['Сбер', 'Яндекс', 'Ростелеком', 'Газпром нефть', 'Авито', 'Тинькофф']
        companies = []
        for name in company_names:
            company = Company.objects.create(
                name=name,
                description=fake.text(max_nb_chars=200),
                industry=fake.word()
            )
            companies.append(company)

        print(" vacancy Создание вакансий...")
        vacancies = []
        for _ in range(10):
            vacancy = Vacancy.objects.create(
                company=choice(companies),
                title=fake.job(),
                description=fake.text(),
                field=choice(fields),
                salary_min=choice([0, 60000, 80000, 100000]),
                salary_max=choice([120000, 150000, 200000]),
                experience=choice(['no', '1-3', '3-5']),
                employment_type=choice(['full', 'internship', 'project']),
                schedule=choice(['office', 'remote', 'hybrid']),
                requirements='<p>Знание Python и Django</p>',
                responsibilities='<p>Разработка API и поддержка сервисов</p>',
                conditions='<p>Офис в центре, ДМС, гибкий график</p>',
                city='Москва',
                address=fake.address(),
                is_active=True
            )
            vacancies.append(vacancy)

    print("✅ Фейковые данные успешно загружены!")

if __name__ == '__main__':
    seed_data()