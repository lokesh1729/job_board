from django.contrib import admin

from job.models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass
