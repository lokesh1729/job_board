import django_filters
from django_select2.forms import ModelSelect2MultipleWidget
from .models import Job, Skill


class HomepageFilter(django_filters.FilterSet):
    min_salary = django_filters.NumberFilter(
        field_name="min_salary", lookup_expr="gte", label="Min Salary"
    )
    max_salary = django_filters.NumberFilter(
        field_name="max_salary", lookup_expr="lte", label="Max Salary"
    )
    skills_required = django_filters.MultipleChoiceFilter(
        field_name="skills_required",
        lookup_expr="name__exact",
        label="Skills",
        widget=ModelSelect2MultipleWidget(
            model=Skill, search_fields=["name__icontains"]
        ),
    )

    class Meta:
        model = Job
        fields = ["remote", "job_type", "min_salary", "max_salary", "skills_required"]
