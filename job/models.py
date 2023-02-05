import random
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings

from candidate.models import Candidate
from recruiter.models import Recruiter, Company
from .constants import JobType, Remote, JobStatus
from common.models import BaseModel, SlugModel, Skill

JOB_STATUS_CHOICES = (
    (JobStatus.ACTIVE.name, JobStatus.ACTIVE.value),
    (JobStatus.EXPIRED.name, JobStatus.EXPIRED.value),
)


class Category(BaseModel, SlugModel):
    name = models.CharField(_("Category Name"), max_length=100)


class Job(BaseModel):

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
        help_text=_(
            "The details of the company such as about, size, industry etc... will be populated on the job page. If no company is shown, create a new company from the dashboard"
        ),
    )
    external_url = models.URLField(_("External URL"), blank=True, null=True)
    job_description = models.TextField(
        _("Job Description"),
    )
    job_title = models.CharField(
        _("Job Title"),
        max_length=100,
        help_text="This will be displayed as the title of the web page.",
    )
    position = models.CharField(
        _("Position"),
        max_length=100,
        help_text="Example : Account Executive, Software Engineer",
    )
    job_type = models.CharField(_("Job Type"), choices=JOB_TYPE_CHOICES, max_length=100)
    min_yoe_required = models.IntegerField(_("Minimum years of experience required"))
    min_salary = models.BigIntegerField(_("Min Salary in USD"))
    max_salary = models.BigIntegerField(_("Max Salary in USD"))
    location = models.CharField(_("Job Location"), max_length=255)
    skills_required = models.ManyToManyField(
        Skill, related_name="jobs", related_query_name="jobs"
    )
    remote = models.CharField(_("Remote?"), choices=REMOTE_CHOICES, max_length=100)
    slug = models.SlugField(_("Slug"), primary_key=True)
    status = models.CharField(
        _("Status"),
        choices=JOB_STATUS_CHOICES,
        max_length=25,
        default=JobStatus.ACTIVE.name,
    )
    active_till = models.DateTimeField(_("Active Till"))
    categories = models.ManyToManyField(
        Category, related_name="jobs", related_query_name="jobs"
    )

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = slugify(
                "%s-%s-%s"
                % (
                    self.company.slug,
                    self.position,
                    random.randint(0, 10000),
                )
            )
            self.active_till = timezone.now() + timezone.timedelta(
                days=settings.DEFAULT_JOB_ACTIVE_IN_DAYS
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug


class JobApplication(BaseModel):
    job = models.ForeignKey(
        Job,
        related_name="job_applications",
        related_query_name="job_application",
        on_delete=models.CASCADE,
    )
    candidate = models.ForeignKey(
        Candidate,
        related_name="job_applications",
        related_query_name="job_application",
        on_delete=models.CASCADE,
    )


class JobStatusHistory(BaseModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    old_status = models.CharField(max_length=25, choices=JOB_STATUS_CHOICES)
    new_status = models.CharField(max_length=25, choices=JOB_STATUS_CHOICES)
