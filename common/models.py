import random
from django.db import models
from django.utils.translation import gettext_lazy as _
from cities_light.models import Country, City

from django.utils.text import slugify


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class School(BaseModel):
    name = models.CharField(_("School Name"), max_length=255)
    country = Country(_("Country"))
    state = models.CharField(_("State"), max_length=100)
    city = City(_("City"), max_length=100)
    address = models.CharField(_("Address"), max_length=255, blank=True, null=True)
    is_enabled = models.BooleanField(_("Is Enabled"), default=True, editable=False)
    slug = models.SlugField(
        _("School Slug"), max_length=100, primary_key=True, editable=False
    )

    def __str__(self):
        return "%s - %s - %s" % (self.name, self.country, self.city)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = slugify(self.name)
            if self.objects.filter(slug=self.slug).exists():
                self.slug = "%s-%s" % (self.slug, random.randint(0, 100000))
        super().save(*args, **kwargs)


class Skill(BaseModel):
    name = models.CharField(_("Skill Name"), max_length=100, primary_key=True)
    slug = models.SlugField(
        _("Skill Slug"), max_length=100, primary_key=True, editable=False
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
