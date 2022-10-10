from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, TemplateView

from common.mixins import LoginRedirectMixin

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_object(self, queryset=None):
        passed_username = self.kwargs.get(self.slug_url_kwarg)
        curr_username = self.request.user.username
        if (
            User.objects.filter(username=passed_username).exists()
            and passed_username != curr_username
        ):
            raise PermissionDenied
        return super().get_object(queryset)


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, LoginRedirectMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class UserSignupView(TemplateView, LoginRedirectMixin):
    template_name = "pages/signup.html"
