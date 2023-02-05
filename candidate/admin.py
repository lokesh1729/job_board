from django.contrib import admin
from candidate.models import (
    Candidate,
    CandidateEducation,
    CandidateExperience,
    CandidatePreference,
    CandidateMisc,
    CandidateProject,
    CandidateSkill,
    Alert,
)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    pass


@admin.register(CandidateEducation)
class CandidateEducationAdmin(admin.ModelAdmin):
    pass


@admin.register(CandidateExperience)
class CandidateExperienceAdmin(admin.ModelAdmin):
    pass


@admin.register(CandidatePreference)
class CandidatePreferenceAdmin(admin.ModelAdmin):
    pass


@admin.register(CandidateMisc)
class CandidateMiscAdmin(admin.ModelAdmin):
    pass


@admin.register(CandidateProject)
class CandidateProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(CandidateSkill)
class CandidateSkillAdmin(admin.ModelAdmin):
    pass


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    pass
