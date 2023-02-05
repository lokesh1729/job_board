from django.contrib import admin

from job.models import Job, Category, JobApplication, JobStatusHistory


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(JobStatusHistory)
class JobStatusHistoryAdmin(admin.ModelAdmin):
    pass
