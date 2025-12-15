from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from main.models import Company, FieldOfStudy, Vacancy

User = get_user_model()

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Удаление старых данных...')
        models = [Vacancy, User, Company, FieldOfStudy]
        for model in models:
            model.objects.all().delete()

        self.stdout.write('Создание направлений подготовки...')
        fields = {}
        field_names = ["Информатика", "Экономика", "Менеджмент", "Юриспруденция", "Лингвистика"]
        for name in field_names:
            field = FieldOfStudy.objects.create(name=name)
            fields[name] = field

        self.stdout.write('Создание компаний...')
        companies = {}
        company_data = [
            ("Яндекс", "Крупная IT-компания", "IT"),
            ("Сбер", "Финансовый холдинг", "Финансы"),
            ("Газпром", "Энергетика", "Энергетика"),
            ("Роснефть", "Нефть и газ", "Энергетика"),
            ("МТС", "Телекоммуникации", "Телеком"),
        ]
        for name, desc, industry in company_data:
            company = Company.objects.create(
                name=name,
                description=desc,
                industry=industry
            )
            companies[name] = company

        self.stdout.write('Создание пользователей...')
        users = {}
        user_data = [
            ("Анна Сидорова", "anna@yandex.ru", "partner", "Яндекс"),
            ("Иван Петров", "ivan@sber.ru", "partner", "Сбер"),
            ("admin", "admin@careercenter.ru", "admin", None),
        ]
        for full_name, email, role, company_name in user_data:
            company = companies.get(company_name) if company_name else None
            user = User.objects.create_user(
                email=email,
                full_name=full_name,
                role=role,
                company=company,
                password="password123"
            )
            users[email] = user

        self.stdout.write('Создание вакансий...')
        vacancy_data = [
            ("Python-разработчик", "Яндекс", "Информатика", 150000, 250000),
            ("Data Scientist", "Яндекс", "Информатика", 200000, 300000),
            ("Финансовый аналитик", "Сбер", "Экономика", 100000, 180000),
            ("Юрист", "Газпром", "Юриспруденция", 120000, 200000),
        ]
        for title, comp_name, field_name, min_sal, max_sal in vacancy_data:
            Vacancy.objects.create(
                title=title,
                description=f"Описание вакансии {title}",
                company=companies[comp_name],
                field=fields[field_name],
                is_active=True,
                salary_min=min_sal,
                salary_max=max_sal,
                city="Москва",
                address="ул. Ленина, д. 1",
                employment_type="full",
                experience="1-3",
                schedule="Полный день",
                requirements="Опыт 2+ года",
                responsibilities="Разработка, тестирование",
                conditions="ДМС, обучение"
            )

        self.stdout.write(
            self.style.SUCCESS('База данных успешно заполнена тестовыми данными!')
        )