from django.contrib import admin
from .models import Company, Recruiter


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    pass
