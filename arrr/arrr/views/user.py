from hashlib import md5

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView

from ..forms import UserRegisterForm
from ..forms import Reservation


class UserRegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "registration/register.html"
    success_message = _("Registration successful, you can log in now.")

    def get_success_url(self):
        return reverse("home")


class UserDetailView(DetailView):
    model = User
    template_name = "user/detail.html"
    slug_field = "username"
    slug_url_kwars = "slug"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.get_object()
        now = timezone.now()
        reservations = Reservation.objects.filter(reserver=user, status="a")
        if not self.request.user.is_staff:
            reservations = reservations.filter(is_public=True)
        ctx['past_rsvs'] = reservations.filter(start__lt=now)
        ctx['upcoming_rsvs'] = reservations.filter(end__gt=now)
        ctx['avatar_md5'] = md5(user.email.encode("utf-8")).hexdigest()
        return ctx
