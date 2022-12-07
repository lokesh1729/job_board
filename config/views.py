"""
contains home page view
"""

from django.views.generic import TemplateView
from job.models import Job

from recruiter import repositories
from common.mixins import LoginRedirectMixin
from job.filters import HomepageFilter


class HomepageView(LoginRedirectMixin, TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = HomepageFilter(self.request.GET, queryset=Job.objects.all())
        return {
            **context,
            "jobs": repositories.list_jobs(queryset=filter.qs),
            "filter_form": filter.form,
        }
