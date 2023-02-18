"""
contains home page view
"""
from django.core.paginator import Paginator
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from common.mixins import LoginRedirectMixin
from job.filters import HomepageFilter
from job.models import Job
from recruiter import repositories


class HomepageView(LoginRedirectMixin, TemplateView):
    template_name = "pages/home.html"
    page_kwarg = "page"
    paginate_by = 10
    paginate_orphans = 0
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = HomepageFilter(self.request.GET, queryset=Job.objects.all())
        queryset = repositories.list_jobs(
            queryset=Job.objects.filter(pk__in=filter.qs.values_list("pk", flat=True))
        )
        paginator = Paginator(
            queryset,
            self.paginate_by,
            orphans=self.paginate_orphans,
            allow_empty_first_page=self.allow_empty,
        )
        page = self.request.GET.get(self.page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == "last":
                page_number = paginator.num_pages
            else:
                raise Http404(
                    _("Page is not “last”, nor can it be converted to an int.")
                )
        try:
            page = paginator.page(page_number)
        except paginator.InvalidPage as e:
            raise Http404(
                _("Invalid page (%(page_number)s): %(message)s")
                % {"page_number": page_number, "message": str(e)}
            )
        return {
            **context,
            "jobs": page.object_list,
            "filter_form": filter.form,
            "paginator": paginator,
            "page_obj": page,
            "is_paginated": page.has_other_pages(),
            "elided_pages": page.paginator.get_elided_page_range(),
        }
