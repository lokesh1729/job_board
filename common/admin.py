"""
admin
"""
from django.contrib import admin
from common.models import School, Skill


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    pass


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass
