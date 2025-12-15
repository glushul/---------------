from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ObjectDoesNotExist
from . import models, forms, serializers
from rest_framework import viewsets

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer

class VacancyViewSet(viewsets.ModelViewSet):
    queryset = models.Vacancy.objects.all()
    serializer_class = serializers.VacancySerializer

def main(request):
    return redirect("vacancies")
    
def get_vacancies(request):
    vacancies = models.Vacancy.objects.filter(info__is_active=True).select_related('info', 'company')

    query_position = request.GET.get("position")
    if query_position:
        vacancies = vacancies.filter(info__title__icontains = query_position)

    query_specialization = request.GET.get("specialization")
    if query_specialization and query_specialization != "-1":
        try:
            field = models.FieldOfStudy.objects.get(id=query_specialization)
            vacancies = vacancies.filter(info__field=field)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("Invalid specialization")
        
    query_employment_type = request.GET.get("employment_type")
    if query_employment_type and query_employment_type != "-1":
        valid_values = {choice[0] for choice in models.EMPLOYMENT_TYPE_CHOICES}
        if query_employment_type not in valid_values:
            return HttpResponseBadRequest("Invalid employment type")
        else:
            vacancies = vacancies.filter(info__employment_type=query_employment_type)

    query_experience = request.GET.get("experience")
    if query_experience and query_experience != "-1":
        valid_values = {choice[0] for choice in models.EXPERIENCE_CHOICES}
        if query_experience not in valid_values:
            return HttpResponseBadRequest("Invalid experience choice")
        else: 
            vacancies = vacancies.filter(info__experience=query_experience)

    data = []
    for v in vacancies:
        data.append({
            "id": v.id,
            "title": v.info.title if v.info else "Без названия",
            "description": v.info.description if v.info else "",
            "company": {
                "name": v.company.name,
                "description": v.company.description,
                "industry": v.company.description,
                "logo": v.company.logo
            },
            "salary_min": v.info.salary_min,
            "salary_max": v.info.salary_max,
            "experience": v.info.experience,
            "education_level": v.info.education_level,
            "employment_type": v.info.employment_type,
            "schedule": v.info.schedule,
            "city": v.info.city,
            "address": v.info.address,
            "created_at": v.created_at.isoformat() if v.created_at else None,
        })

    fields = models.FieldOfStudy.objects.all() 

    context = {
        "vacancies": data,
        "fields": fields,
        "employment_type_choices": models.EMPLOYMENT_TYPE_CHOICES,
        "experience_choices": models.EXPERIENCE_CHOICES,
    }

    return render(request, "vacancies.html", context)

def get_vacancy(request, id):
    v = models.Vacancy.objects.filter(id=id).select_related('info', 'company').first()

    if v is None:
        return HttpResponseBadRequest("Invalid company ID")

    context = {
        "id": v.id,
        "is_active": v.info.is_active,
        "title": v.info.title if v.info else "Без названия",
        "description": v.info.description if v.info else "",
        "company": {
            "name": v.company.name,
            "description": v.company.description,
            "industry": v.company.description,
            "logo": v.company.logo
        },
        "salary_min": v.info.salary_min,
        "salary_max": v.info.salary_max,
        "city": v.info.city,
        "address": v.info.address,
        "employment_type": v.info.employment_type,
        "schedule": v.info.schedule,
        "requirements": v.info.requirements,
        "responsibilities": v.info.responsibilities,
        "conditions": v.info.conditions,
        "created_at": v.created_at if v.created_at else None
    }

    return render(request, "vacancy.html", {"v": context})

def edit_vacancy(request, id):
    if id == "new":
        if request.method == "POST":
            form = forms.VacancyForm(request.POST)
            if form.is_valid():
                vacancy_info = form.save()
                vacancy = models.Vacancy.objects.create(
                    info=vacancy_info,
                    company=request.user.company,
                    irs_active=form.cleaned_data.get('is_active', True)
                )
                return redirect("get_vacancy", id=vacancy.id)
            else:
                return render(request, "edit_vacancy.html", {"form": form, "is_new": True})
        else:
            form = forms.VacancyForm()
            return render(request, "edit_vacancy.html", {"form": form, "is_new": True})
    else:
        if not id.isdigit():
            return HttpResponseBadRequest("Invalid vacancy ID")

        v = get_object_or_404(models.Vacancy, id=id)
        
        if request.method == "POST":
            form = forms.VacancyForm(request.POST, instance=v.info)
            if form.is_valid():
                form.save()
                v.is_active = form.cleaned_data.get('is_active', v.is_active)
                v.save()
                return redirect("get_vacancy", id=v.id)
            else:
                return render(request, "edit_vacancy.html", {"form": form, "v": v})
        else:
            if not hasattr(v, 'info') or v.info is None:
                vacancy_info = models.VacancyInfo.objects.create()
                v.info = vacancy_info
                v.save()
            form = forms.VacancyForm(instance=v.info)
            return render(request, "edit_vacancy.html", {"form": form, "v": v})
        
def get_companies(request):
    companies = models.Company.objects.all()
    return render(request, "companies.html", {"companies": companies})

def edit_company(request, id):
    company = None
    if id != "new":
        company = get_object_or_404(models.Company, id=id)

    user = models.User.objects.filter(company=company).first()

    if request.method == "POST":
        company_form = forms.CompanyForm(request.POST, request.FILES, instance=company)
        user_form = forms.UserCreationForm(request.POST)

        if company_form.is_valid():
            company = company_form.save()
            if user_form.is_valid():
                user = user_form.save(commit=False, company=company)
                user.role =  "partner"
                user.save()
            return redirect("companies")
    else:
        company_form = forms.CompanyForm(instance=company)
        user_form = forms.UserCreationForm(instance=user)

    return render(request, "edit_company.html", {
        "company_form": company_form,
        "user_form": user_form,
        "company": company
    })