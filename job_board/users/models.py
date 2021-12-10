from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    DateTimeField,
    ImageField,
    Model,
    OneToOneField,
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from . import constants


class User(AbstractUser):
    """Default user for Job Board."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class UserProfile(Model):
    ROLE_CHOICES = (
        ("CANDIDATE", constants.Role.CANDIDATE),
        ("EMPLOYER", constants.Role.EMPLOYER),
    )
    user = OneToOneField(
        User,
        on_delete=CASCADE,
        related_name="profile",
        related_query_name="profile",
    )
    avatar = ImageField(_("Avatar"), blank=True, null=True)
    role = CharField(_("Role"), choices=ROLE_CHOICES)
    location = CharField(_("Location"), max_length=100, blank=True, null=True)
    dob = DateField(null=True, blank=True)
    created_on = DateTimeField(auto_now_add=True)
    updated_on = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("UserProfile")
        verbose_name_plural = _("UserProfiles")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("UserProfile_detail", kwargs={"pk": self.pk})
