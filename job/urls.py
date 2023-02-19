from django.urls import path

from .views import JobView

urlpatterns = [
    path("", JobView.as_view(), name="new_job"),
    path("latest_jobs", JobView.as_view(), name="latest_jobs"),
]

app_name = "job"
