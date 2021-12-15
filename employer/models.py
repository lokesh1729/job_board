from django.db import models
from django.utils.translation import gettext_lazy as _
from candidate.models import Skill

from job_board.users.models import UserProfile

from .constants import Remote


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class Employer(BaseModel):
    class Meta:
        abstract = False

    name = models.CharField(_("Employer Name"), max_length=100)
    industry = models.CharField(_("Industry"), max_length=100)


class Recruiter(BaseModel):
    class Meta:
        abstract = False

    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    employer = models.ForeignKey(
        Employer,
        on_delete=models.CASCADE,
        related_name="employees",
        related_query_name="employee",
    )
    employee_id = models.CharField(_("Employee ID"), max_length=100)


class Job(BaseModel):
    class Meta:
        abstract = False

    REMOTE_CHOICES = (
        (Remote.FULLY_REMOTE.name, Remote.FULLY_REMOTE.value),
        (Remote.HYBRID.name, Remote.HYBRID.value),
        (Remote.NO_REMOTE.name, Remote.NO_REMOTE.value),
    )

    posted_by = models.ForeignKey(
        Recruiter,
        on_delete=models.CASCADE,
        related_name="jobs",
        related_query_name="job",
    )
    company = models.ForeignKey(
        Employer,
        on_delete=models.CASCADE,
        related_name="jobs",
        related_query_name="job",
    )
    external_url = models.URLField(_("External URL"), blank=True, null=True)
    job_description = models.TextField(
        _("Job Description"), blank=True, null=True
    )
    min_yoe_required = models.IntegerField(_("Min YOE required"))
    max_salary = models.BigIntegerField(_("Max Salary in USD"))
    location = models.CharField(_("Job Location"), max_length=255)
    skills_required = models.ManyToManyField(Skill)
    remote = models.CharField(
        _("Remote?"), choices=REMOTE_CHOICES, max_length=100
    )
