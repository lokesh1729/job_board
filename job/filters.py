import django_filters
from .models import Job


class HomepageFilter(django_filters.FilterSet):
    min_salary = django_filters.NumberFilter(
        field_name="min_salary", lookup_expr="gte", label="Min Salary"
    )
    max_salary = django_filters.NumberFilter(
        field_name="min_salary", lookup_expr="lte", label="Max Salary"
    )

    class Meta:
        model = Job
        fields = ["remote", "job_type", "min_salary", "max_salary"]
