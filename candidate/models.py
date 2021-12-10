from django.db import models
from django.utils.translation import gettext_lazy as _

from job_board.users.models import UserProfile

from .constants import Proficiency


class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class Candidate(BaseModel):
    class Meta:
        abstract = True

    resume = models.FilePathField()
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)


class School(BaseModel):
    class Meta:
        abstract = True

    name = models.CharField(_("School Name"), max_length=255)
    country = models.CharField(_("Country"), max_length=100)
    state = models.CharField(_("State"), max_length=100)


class CandidateEducation(BaseModel):
    class Meta:
        abstract = True

    candidate = models.ForeignKey(Candidate)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="candidate_educations",
        related_query_name="candidate_education",
    )
    degree = models.CharField(_("Degree"))
    from_date = models.DateField(_("From Date"))
    to_date = models.DateField(_("To Date"))


class CandidateExperience(BaseModel):
    class Meta:
        abstract = True

    candidate = models.ForeignKey(Candidate)
    from_date = models.DateTime(_("From Date"))
    to_date = models.DateField(_("To Date"))
    company = models.CharField(_("Company Name"), max_length=255)
    role = models.CharField(_("Role"), max_length=255)
    responsibilities = models.TextField(_("Responsibilities"))


class Skill(BaseModel):
    class Meta:
        abstract = True

    name = models.CharField(_("Skill Name"), max_length=100)


class CandidateSkill(BaseModel):
    class Meta:
        abstract = True

    PROFICIENCY_CHOICES = (
        (1, Proficiency.ONE),
        (2, Proficiency.TWO),
        (3, Proficiency.THREE),
        (4, Proficiency.FOUR),
        (5, Proficiency.FIVE),
        (6, Proficiency.SIX),
        (7, Proficiency.SEVEN),
        (8, Proficiency.EIGHT),
        (9, Proficiency.NINE),
        (10, Proficiency.TEN),
    )

    candidate = models.ForeignKey(Candidate)
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="candidate_skills",
        related_query_name="candidate_skill",
    )
    proficiency = models.IntegerField(
        _("Proficiency"), choices=PROFICIENCY_CHOICES
    )
    yoe = models.IntegerField(_("Years of Experience"))


class CandidateProject(BaseModel):
    class Meta:
        abstract = True

    candidate = models.ForeignKey(Candidate)
    name = models.CharField(_("Project Name"), max_length=255)
    description = models.TextField(_("Project Description"))
    skills_used = models.ManyToManyField(Skill)


class CandidateMisc(BaseModel):
    class Meta:
        abstract = True

    achievements = models.TextField(
        _("Candidate Achievements"), blank=True, null=True
    )
    awards = models.TextField(_("Candidate Awards"), blank=True, null=True)
