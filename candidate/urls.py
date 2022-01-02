from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.CandidateDashboardView.as_view(), name="dashboard"),
    path("signup/", views.CandidateSignupView.as_view(), name="signup"),
    path("onboarding/", views.CandidateOnboardingView.as_view(), name="onboarding")
]
app_name = "candidate"
