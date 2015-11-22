from django.core.urlresolvers import reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)


from braces.views import LoginRequiredMixin

from ..models import Reservation
from ..forms import ReservationForm


class ReservationListView(ListView):
    model = Reservation
    template_name = "reservation/list.html"


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "reservation/create.html"

    def form_valid(self, form):
        room = form.save(commit=False)
        room.reserver = self.request.user
        return super().form_valid(form)


class ReservationDetailView(DetailView):
    model = Reservation
    template_name = "reservation/detail.html"


class ReservationEditView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "reservation/edit.html"


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = "base/delete.html"

    def get_success_url(self):
        return reverse("reservation/list")
