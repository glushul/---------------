from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render

from . import forms, models
from .resources import VacancyResource


def main(request):
    return redirect("vacancies")


def get_vacancies(request):
    vacancies = models.Vacancy.objects.filter(is_active=True).select_related("company")

    query_position = request.GET.get("position")
    if query_position:
        vacancies = vacancies.filter(title__icontains=query_position)

    query_specialization = request.GET.get("specialization")
    if query_specialization and query_specialization != "-1":
        try:
            field = models.FieldOfStudy.objects.get(id=query_specialization)
            vacancies = vacancies.filter(field=field)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("Invalid specialization")

    query_employment_type = request.GET.get("employment_type")
    if query_employment_type and query_employment_type != "-1":
        valid_values = {choice[0] for choice in models.EMPLOYMENT_TYPE_CHOICES}
        if query_employment_type not in valid_values:
            return HttpResponseBadRequest("Invalid employment type")
        else:
            vacancies = vacancies.filter(employment_type=query_employment_type)

    query_experience = request.GET.get("experience")
    if query_experience and query_experience != "-1":
        valid_values = {choice[0] for choice in models.EXPERIENCE_CHOICES}
        if query_experience not in valid_values:
            return HttpResponseBadRequest("Invalid experience choice")
        else:
            vacancies = vacancies.filter(experience=query_experience)

    data = []
    for v in vacancies:
        vacancy_dict = model_to_dict(v)
        vacancy_dict["company"] = model_to_dict(v.company)
        data.append(vacancy_dict)

    fields = models.FieldOfStudy.objects.all()

    context = {
        "vacancies": data,
        "fields": fields,
        "employment_type_choices": models.EMPLOYMENT_TYPE_CHOICES,
        "experience_choices": models.EXPERIENCE_CHOICES,
    }

    return render(request, "vacancies.html", context)


def get_vacancy(request, id):
    v = models.Vacancy.objects.filter(id=id).select_related("company").first()
    vacancy_dict = model_to_dict(v)
    vacancy_dict["company"] = model_to_dict(v.company)
    return render(request, "vacancy.html", {"v": vacancy_dict})


def edit_vacancy(request, id):
    if id == "new":
        if request.method == "POST":
            form = forms.VacancyForm(request.POST)
            if form.is_valid():
                vacancy = form.save()
                return redirect("get_vacancy", id=vacancy.id)
            else:
                return render(
                    request, "edit_vacancy.html", {"form": form, "is_new": True}
                )
        else:
            form = forms.VacancyForm()
            return render(request, "edit_vacancy.html", {"form": form, "is_new": True})
    else:
        if not id.isdigit():
            return HttpResponseBadRequest("Invalid vacancy ID")

        v = get_object_or_404(models.Vacancy, id=id)

        if request.method == "POST":
            form = forms.VacancyForm(request.POST, instance=v)
            if form.is_valid():
                form.save()
                return redirect("get_vacancy", id=v.id)
            else:
                return render(request, "edit_vacancy.html", {"form": form, "v": v})
        else:
            form = forms.VacancyForm(instance=v)
            return render(request, "edit_vacancy.html", {"form": form, "v": v})


def get_companies(request):
    companies = models.Company.objects.all()
    return render(request, "companies.html", {"companies": companies})


def edit_company(request, id):
    company = None
    if id != "new":
        company = get_object_or_404(models.Company, id=id)

    if request.method == "POST":
        company_form = forms.CompanyForm(request.POST, request.FILES, instance=company)
        if company_form.is_valid():
            company = company_form.save()
            return redirect("companies")
    else:
        company_form = forms.CompanyForm(instance=company)

    return render(
        request, "edit_company.html", {"form": company_form, "company": company}
    )


def export_vacancies_xlsx(request, company_id):
    vacancies = models.Vacancy.objects.filter(
        Q(company_id=company_id) & Q(is_active=True)
    )

    dataset = VacancyResource().export(queryset=vacancies)
    response = HttpResponse(
        dataset.xlsx,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = (
        f'attachment; filename="vacancies_{company_id}.xlsx"'
    )
    return response

def delete_vacancy(request, id):
    vacancy = get_object_or_404(models.Vacancy, id=id)
    vacancy.delete()
    return redirect('vacancies')  