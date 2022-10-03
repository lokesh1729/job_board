from django.db import models
from django.utils.translation import gettext_lazy as _
from candidate.models import Skill

from recruiter.models import Recruiter, Company
from .constants import JobType, Remote
from common.models import BaseModel


class Job(BaseModel):
    class Meta:
        abstract = False

    REMOTE_CHOICES = (
        (Remote.FULLY_REMOTE.name, Remote.FULLY_REMOTE.value),
        (Remote.HYBRID.name, Remote.HYBRID.value),
        (Remote.NO_REMOTE.name, Remote.NO_REMOTE.value),
    )

    JOB_TYPE_CHOICES = (
        (JobType.FULL_TIME.name, JobType.FULL_TIME.value),
        (JobType.PART_TIME.name, JobType.PART_TIME.value),
        (JobType.CONTRACT.name, JobType.CONTRACT.value),
    )

    posted_by = models.ForeignKey(
        Recruiter,
        on_delete=models.CASCADE,
        related_name="jobs",
        related_query_name="job",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="jobs",
        related_query_name="job",
        help_text=_("The details of the company such as about, size, industry etc... will be populated on the job page. If no company is shown, create a new company from the dashboard")
    )
    external_url = models.URLField(_("External URL"), blank=True, null=True)
    job_description = models.TextField(
        _("Job Description"),
    )
    job_title = models.CharField(_("Job Title"), max_length=100, help_text="This will be displayed on the web page.")
    position = models.CharField(_("Position"), max_length=100, help_text="Example : Account Executive, Software Engineer")
    job_type = models.CharField(_("Job Type"), choices=JOB_TYPE_CHOICES, max_length=100)
    min_yoe_required = models.IntegerField(_("Minimum years of experience required"))
    min_salary = models.BigIntegerField(_("Min Salary in USD"))
    max_salary = models.BigIntegerField(_("Max Salary in USD"))
    location = models.CharField(_("Job Location"), max_length=255)
    skills_required = models.ManyToManyField(Skill)
    remote = models.CharField(
        _("Remote?"), choices=REMOTE_CHOICES, max_length=100
    )
