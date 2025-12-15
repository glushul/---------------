from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

ROLE_CHOICES = (
    ('admin', 'Администратор'),
    ('partner', 'Компания-партнер'),
    ('student', 'Студент'),
)

EMPLOYMENT_TYPE_CHOICES = (
    ('full', 'Полная занятость'),
    ('part', 'Частичная занятость'),
    ('project', 'Проектная работа'),
)

EXPERIENCE_CHOICES = (
    ('no', 'Нет опыта'),
    ('1', 'До 1 года'),
    ('1-3', '1–3 года'),
    ('3+', 'Более 3 лет'),
)

class Company(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", blank=True)
    industry = models.CharField("Индустрия", max_length=100, blank=True)
    logo = models.ImageField("Логотип", upload_to='logos/', blank=True, null=True)

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self):
        return self.name


class FieldOfStudy(models.Model):
    name = models.CharField("Название направления", max_length=100, unique=True)

    class Meta:
        verbose_name = "Направление подготовки"
        verbose_name_plural = "Направления подготовки"

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # ❗️Обратите внимание: принимаем username, но не используем
        username = extra_fields.pop('username', None)  # игнорируем username
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField("Электронная почта", unique=True)
    full_name = models.CharField("Полное имя", max_length=255)
    role = models.CharField("Роль", max_length=20, choices=ROLE_CHOICES)
    company = models.ForeignKey(
        Company,
        verbose_name="Компания",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'role']

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Vacancy(models.Model):
    title = models.CharField("Название вакансии", max_length=255)
    description = models.TextField("Краткое описание")
    company = models.ForeignKey(
        Company,
        verbose_name="Компания",
        on_delete=models.CASCADE,
        related_name="vacancies"
    )
    field = models.ForeignKey(
        FieldOfStudy,
        verbose_name="Направление",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField("Активна", default=True)
    salary_min = models.PositiveIntegerField("Зарплата от", null=True, blank=True)
    salary_max = models.PositiveIntegerField("Зарплата до", null=True, blank=True)
    city = models.CharField("Город", max_length=100, blank=True)
    address = models.CharField("Адрес", max_length=255, blank=True)
    employment_type = models.CharField(
        "Тип занятости",
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        blank=True
    )
    experience = models.CharField(
        "Опыт работы",
        max_length=10,
        choices=EXPERIENCE_CHOICES,
        blank=True
    )
    schedule = models.CharField("График работы", max_length=100, blank=True)

    requirements = models.TextField("Требования", blank=True)
    responsibilities = models.TextField("Обязанности", blank=True)
    conditions = models.TextField("Условия", blank=True)

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} в {self.company.name}"
