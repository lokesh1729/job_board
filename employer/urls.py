from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.EmployerDashboardView.as_view(), name="dashboard"),
    path("signup/", views.EmployerSignupView.as_view(), name="signup")
]
app_name = "employer"
