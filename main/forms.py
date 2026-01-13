from django import forms

from . import models


class VacancyForm(forms.ModelForm):
    class Meta:
        model = models.Vacancy
        fields = [
            "title",
            "company",
            "description",
            "field",
            "requirements",
            "responsibilities",
            "conditions",
            "salary_min",
            "salary_max",
            "city",
            "address",
            "employment_type",
            "schedule",
            "is_active",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "company": forms.Select(attrs={'class': 'form-select'}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "field": forms.Select(attrs={"class": "form-select"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "employment_type": forms.Select(attrs={"class": "form-select"}),
            "schedule": forms.Select(attrs={"class": "form-select"}),
            "salary_min": forms.NumberInput(attrs={"class": "form-control"}),
            "salary_max": forms.NumberInput(attrs={"class": "form-control"}),
            "requirements": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "responsibilities": forms.Textarea(
                attrs={"class": "form-control", "rows": 6}
            ),
            "conditions": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = ["name", "description", "industry", "logo"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "industry": forms.TextInput(attrs={"class": "form-control"}),
        }
