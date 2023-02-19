import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms
from django.db.models import Q
from django_select2.forms import ModelSelect2MultipleWidget

from .models import Company, Job, Skill


class TitleDescriptionFilter(django_filters.CharFilter):
    def filter(self, qs, value):
        if value in ([], (), {}, "", None):
            return qs
        return qs.filter(
            Q(job_title__contains=value) | Q(job_description__contains=value)
        )


class JobFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.include_media = False
        self.helper.add_layout(
            layout=Layout(
                "title_or_description",
                Row(Column("remote"), Column("job_type")),
                Row(Column("min_salary"), Column("max_salary")),
                Row(Column("company"), Column("skills_required")),
            )
        )
        super().__init__(*args, **kwargs)


class HomepageFilter(django_filters.FilterSet):
    min_salary = django_filters.NumberFilter(
        field_name="min_salary", lookup_expr="gte", label="Min Salary"
    )
    max_salary = django_filters.NumberFilter(
        field_name="max_salary", lookup_expr="lte", label="Max Salary"
    )
    title_or_description = TitleDescriptionFilter(label="Job Title or Description")
    skills_required = django_filters.ModelMultipleChoiceFilter(
        queryset=Skill.objects.all(),
        field_name="skills_required",
        lookup_expr="exact",
        label="Skills",
        widget=ModelSelect2MultipleWidget(
            model=Skill, search_fields=["name__icontains"]
        ),
    )
    company = django_filters.ModelMultipleChoiceFilter(
        queryset=Company.objects.all(),
        field_name="company",
        # lookup_expr="icontains",
        label="Company",
        widget=ModelSelect2MultipleWidget(
            model=Company, search_fields=["name__icontains"]
        ),
    )

    class Meta:
        model = Job
        fields = [
            "title_or_description",
            "remote",
            "job_type",
            "min_salary",
            "max_salary",
            "skills_required",
            "company",
        ]
        form = JobFilterForm
