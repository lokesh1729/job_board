from django.db import models

class Candidate(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    resume = models.FilePathField()
