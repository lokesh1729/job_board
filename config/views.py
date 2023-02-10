"""
contains home page view
"""

from django.views.generic import TemplateView

from common.mixins import LoginRedirectMixin
from job.constants import Remote
from job.filters import HomepageFilter
from job.models import Job
from recruiter import repositories


class HomepageView(LoginRedirectMixin, TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = HomepageFilter(self.request.GET, queryset=Job.objects.all())
        return {
            **context,
            "latest_jobs": repositories.list_jobs(
                queryset=Job.objects.order_by("-created_on")
            )[:5],
            "popular_jobs": repositories.list_jobs(
                queryset=Job.objects.order_by("-score")
            )[:5],
            "remote_jobs": repositories.list_jobs(
                queryset=Job.objects.filter(remote=Remote.FULLY_REMOTE.name)
            )[:5],
            "filter_form": filter.form,
        }
