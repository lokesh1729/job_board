from django.db import models
from django.utils.translation import gettext_lazy as _
from cities_light.models import City

from job_board.users.models import UserProfile

from common.models import BaseModel, School, Skill

from .constants import Proficiency, JobSearchChoices, ProfilePrivacyChoices


class Candidate(BaseModel):

    resume = models.FileField(upload_to="candidates/resumes")
    onboarding_done = models.BooleanField(default=False)
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    saved_jobs = models.ManyToManyField(
        "job.Job",
        related_name="saved_by_candidates",
        related_query_name="saved_by_candidates",
    )

    def __str__(self):
        return "Candidate : %s : %s" % (self.profile.user.name, self.profile.user.email)


class CandidatePreference(BaseModel):

    JOB_SEARCH_CHOICES = (
        (JobSearchChoices.ACTIVELY_LOOKING, "Actively Looking"),
        (JobSearchChoices.PASSIVELY_LOOKING, "Passively Looking"),
        (JobSearchChoices.NOT_LOOKING, "Not Looking At The Moment"),
    )

    PROFILE_PRIVACY_CHOICES = (
        (ProfilePrivacyChoices.NONE, "No one! Hide from everyone"),
        (ProfilePrivacyChoices.ALL, "Everyone!"),
        (
            ProfilePrivacyChoices.ONLY_TO_WHOSE_JOBS_I_APPLIED_TO,
            "Recruiters to whose jobs I applied!",
        ),
    )

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="candidate_prefs",
        related_query_name="candidate_pref",
    )
    current_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="preferred_candidates",
        related_query_name="preferred_candidate",
    )
    desired_cities = models.ManyToManyField(
        City,
        related_name="desired_candidates",
        related_query_name="desired_candidates",
    )
    expected_salary = models.IntegerField(_("Expected Salary"))
    current_salary = models.IntegerField(_("Expected Salary"))
    job_search_status = models.CharField(
        _("Job Search Status"),
        choices=JOB_SEARCH_CHOICES,
        max_length=100,
    )
    profile_privacy = models.CharField(
        _("Who can see your profile?"), choices=PROFILE_PRIVACY_CHOICES, max_length=100
    )


class CandidateEducation(BaseModel):
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


class CandidateSkill(BaseModel):
    PROFICIENCY_CHOICES = (
        (Proficiency.ONE, Proficiency.ONE),
        (Proficiency.TWO, Proficiency.TWO),
        (Proficiency.THREE, Proficiency.THREE),
        (Proficiency.FOUR, Proficiency.FOUR),
        (Proficiency.FIVE, Proficiency.FIVE),
        (Proficiency.SIX, Proficiency.SIX),
        (Proficiency.SEVEN, Proficiency.SEVEN),
        (Proficiency.EIGHT, Proficiency.EIGHT),
        (Proficiency.NINE, Proficiency.NINE),
        (Proficiency.TEN, Proficiency.TEN),
    )

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
    proficiency = models.IntegerField(_("Proficiency"), choices=PROFICIENCY_CHOICES)
    yoe = models.IntegerField(_("Years of Experience"))


class CandidateProject(BaseModel):
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
    achievements = models.TextField(_("Candidate Achievements"), blank=True, null=True)
    awards = models.TextField(_("Candidate Awards"), blank=True, null=True)


class Alert(BaseModel):
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="alerts",
        related_query_name="alert",
        blank=True,
        null=True,
    )
    name = models.CharField(_("Alert Name"), max_length=100)
    email = models.EmailField(null=True)
    filters = models.TextField(_("Filters"))
