from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView

from ..forms import UserRegisterForm


class UserRegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "registration/register.html"
    success_message = _("Registration successful, you can log in now.")

    def get_success_url(self):
        return reverse("home")
