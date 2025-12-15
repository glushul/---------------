from django.contrib import admin
from . import models
from django.utils.safestring import mark_safe

class VacancyInline(admin.TabularInline):
    model = models.Vacancy
    extra = 0
    fields = ('title', 'is_active', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'vacancy_count', 'logo_preview']
    list_display_links = ['name']
    list_filter = ['industry']
    search_fields = ['name', 'industry']
    inlines = [VacancyInline]
    readonly_fields = ['logo_preview']

    @admin.display(description="Логотип")
    def logo_preview(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" style="max-height: 40px;">')
        return "—"

    @admin.display(description="Вакансий")
    def vacancy_count(self, obj):
        return obj.vacancies.count()


@admin.register(models.FieldOfStudy)
class FieldOfStudyAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class UserInline(admin.TabularInline):
    model = models.User
    extra = 0
    fields = ('full_name', 'email', 'role')
    readonly_fields = ('email',)


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'role', 'company_link']
    list_filter = ['role', 'company']
    search_fields = ['full_name', 'email']
    readonly_fields = ['last_login', 'date_joined']
    raw_id_fields = ['company']
    fieldsets = (
        ('Основное', {'fields': ('email', 'full_name', 'password')}),
        ('Роль и компания', {'fields': ('role', 'company')}),
        ('Даты', {'fields': ('last_login', 'date_joined'), 'classes': ('collapse',)}),
    )

    @admin.display(description="Компания")
    def company_link(self, obj):
        if obj.company:
            return mark_safe(
                f'<a href="/admin/main/company/{obj.company.id}/change/">{obj.company.name}</a>'
            )
        return "—"


@admin.register(models.Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'company_link', 'is_active', 'salary_range', 'city',
        'employment_type', 'created_at'
    ]
    list_display_links = ['title']
    list_filter = [
        'is_active', 'employment_type', 'experience', 'created_at',
        'company__industry'
    ]
    search_fields = ['title', 'description', 'company__name', 'city']
    date_hierarchy = 'created_at'
    raw_id_fields = ['company', 'field']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'description', 'company', 'field', 'is_active')
        }),
        ('Зарплата и локация', {
            'fields': (('salary_min', 'salary_max'), 'city', 'address')
        }),
        ('Условия', {
            'fields': ('employment_type', 'experience', 'schedule')
        }),
        ('Подробности', {
            'fields': ('requirements', 'responsibilities', 'conditions')
        }),
        ('Системное', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description="Компания")
    def company_link(self, obj):
        return mark_safe(
            f'<a href="/admin/main/company/{obj.company.id}/change/">{obj.company.name}</a>'
        )

    @admin.display(description="Зарплата")
    def salary_range(self, obj):
        if obj.salary_min and obj.salary_max:
            return f"{obj.salary_min} – {obj.salary_max}"
        elif obj.salary_min:
            return f"от {obj.salary_min}"
        elif obj.salary_max:
            return f"до {obj.salary_max}"
        return "—"