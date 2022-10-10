"""
contains home page view
"""

from django.views.generic import TemplateView

from recruiter import repositories


class HomepageView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, "jobs": repositories.list_jobs()}
