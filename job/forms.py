"""
Forms
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import Job

class JobForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.role = kwargs.pop("role")
        super().__init__(*args, **kwargs)

    class Meta:
        model = Job
        exclude = ("posted_by", "active_till", "status", "slug")

    def save(self, commit=True):
        self.instance.posted_by=self.role
        return super(JobForm, self).save(commit=commit)

    def clean_min_salary(self):
        if self.cleaned_data["min_salary"] < 0:
            raise ValidationError("minimum salary should be greater than zero")
        return self.cleaned_data["min_salary"]
        
    
    def clean_min_yoe_required(self):
        if self.cleaned_data["min_yoe_required"] < 0:
            raise ValidationError("minimum yoe required should be greater than or equal to zero")
        return self.cleaned_data["min_yoe_required"]

    
    def clean_max_salary(self):
        if self.cleaned_data["max_salary"] < 0:
            raise ValidationError("maximum salary should be greater than zero")
        return self.cleaned_data["max_salary"]
    
    def clean(self):
        if self.cleaned_data["min_salary"] > self.cleaned_data["max_salary"]:
            raise ValidationError("minimum salary should be less than max salary")
        return super().clean()
