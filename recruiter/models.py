from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from cities_light.models import City

from job_board.users.models import UserProfile
from common.models import BaseModel, SlugModel


class Company(BaseModel, SlugModel):
    class Meta:
        abstract = False
        verbose_name_plural = "companies"

    name = models.CharField(_("Company Name"), max_length=125)
    slug = models.SlugField(
        _("Company Slug"), max_length=125, editable=False, primary_key=True
    )
    industry = models.CharField(
        _("Industry"),
        help_text=_(
            "Which industry does it belong to? Examples: Software Engineering, Manufacturing"
        ),
        max_length=100,
    )
    size = models.CharField(
        _("Company Size"), help_text=_("What's the employee headcount?"), max_length=100
    )
    location = models.ForeignKey(
        City,
        related_name="companies",
        related_query_name="company",
        on_delete=models.CASCADE,
    )
    about = models.TextField(
        _("About Company"),
        help_text=_(
            "Write about the company. It will be displayed on the web page to the users."
        ),
    )
    logo = models.ImageField(
        _("Logo of the company"),
        help_text=_("Logo of the company"),
        upload_to="recruiters/company/logo",
    )
    url = models.URLField(_("Website URL"), help_text=_("URL of the company website"))

    def __str__(self):
        return "%s - %s" % (self.name, self.location.display_name)


class Recruiter(BaseModel):

    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    companies = models.ManyToManyField(Company)
