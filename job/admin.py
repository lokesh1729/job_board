from django.contrib import admin

from job.models import Job, Skill


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass
