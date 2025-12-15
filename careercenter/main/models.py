# models.py
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

ROLE_CHOICES = [
    ('student', 'Студент'),
    ('partner', 'Партнёр'),
    ('admin', 'Администратор'),
]

EXPERIENCE_CHOICES = [
    ('no', 'Нет опыта'),
    ('1-3', '1–3 года'),
    ('3-5', '3–5 лет'),
]

EDUCATION_LEVEL_CHOICES = [
    ('high', 'Среднее профессиональное'),
    ('bachelor', 'Бакалавриат'),
    ('master', 'Магистратура'),
    ('student', 'Студент'),
]

EMPLOYMENT_TYPE_CHOICES = [
    ('full', 'Полная занятость'),
    ('part', 'Частичная занятость'),
    ('internship', 'Стажировка'),
    ('project', 'Проектная работа'),
]

SCHEDULE_CHOICES = [
    ('office', 'Офис'),
    ('remote', 'Удалёнка'),
    ('hybrid', 'Гибрид'),
    ('flexible', 'Гибкий график'),
    ('by_agreement', 'По договорённости'),
]

RESPONSE_TYPE_CHOICES = [
    ('internal', 'Внутренний отклик'),
    ('email', 'Email'),
    ('external_link', 'Внешняя ссылка'),
]

APPLICATION_STATUS_CHOICES = [
    ('pending', 'На рассмотрении'),
    ('reviewed', 'Рассмотрено'),
    ('invited', 'Приглашён'),
    ('rejected', 'Отклонено'),
]


class Company(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

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
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return self.email


class FieldOfStudy(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)

    class Meta:
        verbose_name = "Field of Study"
        verbose_name_plural = "Fields of Study"

    def __str__(self):
        return self.name

class VacancyInfo(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False)

    field = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE, related_name='vacancies', null=True)
    is_active = models.BooleanField(default=True)

    salary_min = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    salary_max = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)

    experience = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES, blank=True)
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, blank=True)

    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, blank=True)
    schedule = models.CharField(max_length=20, choices=SCHEDULE_CHOICES, blank=True)

    requirements = models.TextField(help_text="HTML content", blank=True)
    responsibilities = models.TextField(help_text="HTML content", blank=True)
    conditions = models.TextField(help_text="HTML content", blank=True)

    city = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=255, blank=True)

    response_type = models.CharField(max_length=20, choices=RESPONSE_TYPE_CHOICES, null=False, blank=False)
    response_destination = models.CharField(max_length=255, blank=True, help_text="Email или URL при не-internal типе")

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    info = models.ForeignKey(VacancyInfo, on_delete=models.CASCADE, related_name='vacancies')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_vacancies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Vacancy #{self.id} at {self.company.name}"

class Event(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(blank=True)
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    cover_image_url = models.URLField(blank=True, help_text="Обложка мероприятия")

    def __str__(self):
        return self.title

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    resume_file_url = models.URLField(blank=True, help_text="Ссылка на PDF-резюме (если response_type = internal)")
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'vacancy')

    def __str__(self):
        return f"{self.user.full_name} → {self.vacancy.info.title if hasattr(self.vacancy, 'info') else 'Vacancy'}"