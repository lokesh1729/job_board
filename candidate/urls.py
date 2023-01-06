from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.CandidateDashboardView.as_view(), name="dashboard"),
    path("signup/", views.CandidateSignupView.as_view(), name="signup"),
    path(
        "onboarding/preferences",
        views.CandidatePreferenceView.as_view(),
        name="preferences",
    ),
    path(
        "onboarding/education", views.CandidateEducationNew.as_view(), name="education"
    ),
    path("onboarding/work", views.CandidateWorkView.as_view(), name="work"),
    path("onboarding/projects", views.CandidateProjectView.as_view(), name="projects"),
    path("onboarding/skills", views.CandidateSkillView.as_view(), name="skills"),
]
app_name = "candidate"
