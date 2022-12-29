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
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import constants


class UserProfile(Model):
    ROLE_CHOICES = (
        (constants.Role.CANDIDATE.name, constants.Role.CANDIDATE.value),
        (constants.Role.RECRUITER.name, constants.Role.RECRUITER.value),
        (constants.Role.ADMIN.name, constants.Role.ADMIN.value),
    )
    avatar = ImageField(_("Avatar"), blank=True, null=True)
    role = CharField(_("Role"), choices=ROLE_CHOICES, max_length=50)
    location = CharField(_("Location"), max_length=100, blank=True, null=True)
    dob = DateField(null=True, blank=True)
    created_on = DateTimeField(auto_now_add=True)
    updated_on = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("UserProfile")
        verbose_name_plural = _("UserProfiles")

    def __str__(self):
        return "%s - %s" % (self.user, self.role)

    def get_absolute_url(self):
        return reverse("UserProfile_detail", kwargs={"pk": self.pk})


class User(AbstractUser):
    """Default user for Job Board."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    profile = OneToOneField(
        UserProfile,
        on_delete=CASCADE,
        related_name="user",
        related_query_name="user",
    )

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


@receiver(post_save, sender=User)
def callback(signal, sender, instance, **kwargs):
    if (
        kwargs.get("created", False) is True
        and instance.is_staff
        and instance.is_superuser
    ):
        UserProfile.objects.create(user=instance, role=constants.Role.ADMIN.name)
