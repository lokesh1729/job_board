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


class SlugModel(models.Model):
    class Meta:
        abstract = True

    slug = models.SlugField(_("Slug"), max_length=100, primary_key=True, editable=False)

    def save(self, *args, **kwargs):
        if self.pk is None or self.pk == "":
            self.slug = slugify(self.name)
            if self.__class__.objects.filter(slug=self.slug).exists():
                self.slug = "%s-%s" % (self.slug, random.randint(0, 100000))
        super().save(*args, **kwargs)


class School(BaseModel, SlugModel):
    name = models.CharField(_("School Name"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=100, primary_key=True, editable=False)
    country = models.ForeignKey(
        Country,
        related_name="schools",
        related_query_name="school",
        on_delete=models.CASCADE,
        null=True,
    )
    state = models.CharField(_("State"), max_length=100)
    city = models.ForeignKey(
        City,
        related_name="schools",
        related_query_name="school",
        on_delete=models.CASCADE,
    )
    address = models.CharField(_("Address"), max_length=255, blank=True, null=True)
    is_enabled = models.BooleanField(_("Is Enabled"), default=True, editable=False)

    def __str__(self):
        return "%s - %s - %s" % (self.name, self.country, self.city)

    def save(self, *args, **kwargs):
        if self.pk is None or self.pk == "":
            self.slug = slugify(f"{self.name}-{self.country.name}-{self.city.name}")
            if self.__class__.objects.filter(slug=self.slug).exists():
                self.slug = "%s-%s" % (self.slug, random.randint(0, 100000))
        super().save(*args, **kwargs)


class Skill(BaseModel, SlugModel):
    name = models.CharField(_("Skill Name"), max_length=100)

    def __str__(self):
        return self.name
