from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.CandidateDashboardView.as_view(), name="dashboard"),
    path("signup/", views.CandidateSignupView.as_view(), name="signup"),
    # path("onboarding/", views.CandidateOnboardingView.as_view(), name="onboarding"),
    path("onboarding/education", views.candidate_education, name="education"),
    path("onboarding/education", views.education_details, name="education"),
    path("onboarding/work", views.work_details, name="work"),
    path("onboarding/project", views.project_details, name="project"),
    path("onboarding/skill", views.skill_details, name="skill"),
]
app_name = "candidate"
