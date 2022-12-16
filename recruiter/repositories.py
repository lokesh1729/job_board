"""
Repositories
"""
from job.models import Job
from django.conf import settings
from django.db.models.expressions import F
from django.contrib.postgres.aggregates import ArrayAgg


def list_jobs(queryset=None):
    """ """
    if queryset is None:
        queryset = Job.objects.all()
    queryset = (
        queryset.select_related("company")
        .prefetch_related("skills_required")
        .annotate(
            company_name=F("company__name"),
            skills=ArrayAgg("skills_required__name"),
            logo=F("company__logo"),
        )
        .values(
            "position",
            "job_type",
            "min_salary",
            "max_salary",
            "remote",
            "status",
            "slug",
            "created_on",
            "company_name",
            "skills",
            "logo",
        )
    )
    return list(
        map(
            lambda item: {
                **item,
                "logo": "%s/%s" % (settings.MEDIA_URL, item["logo"]),
                "remote": dict(Job.REMOTE_CHOICES).get(item["remote"], ""),
                "job_type": dict(Job.JOB_TYPE_CHOICES).get(item["job_type"], ""),
            },
            queryset,
        )
    )
