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
    User, Company, FieldOfStudy, Vacancy, VacancyInfo,
    Event, Application
)
from faker import Faker
from random import choice, sample

fake = Faker('ru_RU')

def seed_data():
    from django.db import transaction
    with transaction.atomic():
        print("🗑️ Удаление старых данных...")
        Application.objects.all().delete()
        VacancyInfo.objects.all().delete()
        Vacancy.objects.all().delete()
        Event.objects.all().delete()
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
        admin = User.objects.create(email='admin@polytech.ru', full_name='Админ Центра', role='admin')

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
                industry=fake.word(),
                logo="https://proxys.io/files/blog/avito_logo.png"
            )
            companies.append(company)

        print(" vacancy Создание вакансий...")
        vacancies = []
        for _ in range(10):
            vacancy_info = VacancyInfo.objects.create(
                title=fake.job(),
                description=fake.text(),
                field=choice(fields),
                salary_min=choice([0, 60000, 80000, 100000]),
                salary_max=choice([120000, 150000, 200000]),
                experience=choice(['no', '1-3', '3-5']),
                education_level=choice(['bachelor', 'master', 'student']),
                employment_type=choice(['full', 'internship', 'project']),
                schedule=choice(['office', 'remote', 'hybrid']),
                requirements='<p>Знание Python и Django</p>',
                responsibilities='<p>Разработка API и поддержка сервисов</p>',
                conditions='<p>Офис в центре, ДМС, гибкий график</p>',
                city='Москва',
                address=fake.address(),
                response_type='internal'
            )
            vacancy = Vacancy.objects.create(
                company=choice(companies),
                info=vacancy_info,
                is_active=True,
                created_by=partner
            )
            vacancies.append(vacancy)

        print("📅 Создание мероприятий...")
        for _ in range(3):
            Event.objects.create(
                title=fake.sentence(nb_words=3),
                description=fake.text(),
                event_date=fake.future_datetime(end_date="+30d"),
                location='Москва, Стромынка, 26',
                cover_image_url="https://via.placeholder.com/600x300"
            )

        print("📩 Создание откликов...")
        for user in users:
            applied_vacancies = sample(vacancies, k=choice([1, 2]))
            for vac in applied_vacancies:
                Application.objects.create(
                    user=user,
                    vacancy=vac,
                    resume_file_url="https://example.com/resume.pdf",
                    status=choice(['pending', 'reviewed', 'invited'])
                )

    print("✅ Фейковые данные успешно загружены!")

if __name__ == '__main__':
    seed_data()