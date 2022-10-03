from .views import JobView
from django.urls import path


urlpatterns = [
    path("", JobView.as_view(), name="new_job")
]

app_name = "job"
