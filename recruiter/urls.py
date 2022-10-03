from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.RecruiterDashboardView.as_view(), name="dashboard"),
    path("signup/", views.RecruiterSignupView.as_view(), name="signup"),
    path("company/", views.CompanyCreateView.as_view(), name="new_company")
]
app_name = "recruiter"
