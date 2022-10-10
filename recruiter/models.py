from django.db import models
from django.utils.translation import gettext_lazy as _

from job_board.users.models import UserProfile
from common.models import BaseModel


class Company(BaseModel):
    class Meta:
        abstract = False
        verbose_name_plural = "companies"

    name = models.CharField(_("Company Name"), max_length=100)
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
    location = models.CharField(
        _("Company Location"),
        help_text=_("Where is the headquarters located?"),
        max_length=100,
    )
    about = models.TextField(
        _("About Company"),
        help_text=_("Write about the company. It will be displayed on the web page."),
    )
    logo = models.ImageField(
        _("Logo of the company"), help_text=_("Logo of the company")
    )
    url = models.URLField(_("Website URL"), help_text=_("URL of the company website"))

    def __str__(self):
        return self.name


class Recruiter(BaseModel):
    class Meta:
        abstract = False

    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    companies = models.ManyToManyField(Company)
