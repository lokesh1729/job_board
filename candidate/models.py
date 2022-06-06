from django.db import models
from django.utils.translation import gettext_lazy as _

from job_board.users.models import UserProfile

from .constants import Proficiency


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class Candidate(BaseModel):
    class Meta:
        abstract = False

    resume = models.FileField(upload_to="candidates/resumes")
    onboarding_done = models.BooleanField(default=False)
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return "Candidate : %s : %s" % (self.profile.user.name, self.profile.user.email)


class School(BaseModel):
    class Meta:
        abstract = False

    name = models.CharField(_("School Name"), max_length=255)
    country = models.CharField(_("Country"), max_length=100, blank=True, null=True)
    state = models.CharField(_("State"), max_length=100, blank=True, null=True)


class CandidateEducation(BaseModel):
    class Meta:
        abstract = False

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="candidate_educations",
        related_query_name="candidate_education",
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="candidate_educations",
        related_query_name="candidate_education",
    )
    degree = models.CharField(_("Degree"), max_length=100)
    from_date = models.DateField(_("From Date"))
    to_date = models.DateField(_("To Date"))


class CandidateExperience(BaseModel):
    class Meta:
        abstract = False

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="candidate_experiences",
        related_query_name="candidate_experience",
    )
    from_date = models.DateField(_("From Date"))
    to_date = models.DateField(_("To Date"))
    company = models.CharField(_("Company Name"), max_length=255)
    role = models.CharField(_("Role"), max_length=255)
    responsibilities = models.TextField(_("Responsibilities"))


class Skill(BaseModel):
    class Meta:
        abstract = False

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

    name = models.CharField(_("Skill Name"), max_length=100)
    proficiency = models.IntegerField(
        _("Proficiency"), choices=PROFICIENCY_CHOICES, null=True
    )
    yoe = models.IntegerField(_("Years of Experience"), null=True)


class CandidateSkill(BaseModel):
    class Meta:
        abstract = False

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="candidate_skills",
        related_query_name="candidate_skill",
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="candidate_skills",
        related_query_name="candidate_skill",
    )


class CandidateProject(BaseModel):
    class Meta:
        abstract = False

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="candidate_projects",
        related_query_name="candidate_project",
    )
    name = models.CharField(_("Project Name"), max_length=255)
    description = models.TextField(_("Project Description"))
    skills_used = models.ManyToManyField(Skill)


class CandidateMisc(BaseModel):
    class Meta:
        abstract = False

    achievements = models.TextField(_("Candidate Achievements"), blank=True, null=True)
    awards = models.TextField(_("Candidate Awards"), blank=True, null=True)
