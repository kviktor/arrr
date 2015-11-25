from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.utils.translation import ugettext as _
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)


from braces.views import LoginRequiredMixin

from ..models import Reservation, Room
from ..forms import ReservationForm


class ReservationListView(ListView):
    model = Reservation
    template_name = "reservation/list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        reservations = Reservation.objects.all()
        ctx['approved'] = reservations.filter(status="a")
        ctx['pending'] = reservations.filter(status="p")
        return ctx


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
    template_name = "base-delete.html"

    def get_success_url(self):
        return reverse("reservation.list")


@require_POST
def approve_reservation(request, pk):
    res = get_object_or_404(Reservation, pk=pk)

    if not request.user.is_staff:
        raise PermissionDenied

    approve = request.POST.get("approve")
    res.changed_by = request.user
    res.status = "a" if approve is not None else "r"
    if approve is not None:
        messages.success(request, _("Reservation successfully approved."))
    else:
        messages.info(request, _("Reservation successfully rejected."))

    res.save()

    return redirect(reverse("reservation.list"))


@require_GET
def get_calendar_data(request):
    user = request.user

    reservations = Reservation.objects.filter(status="a")
    if not user.is_staff:
        reservations = reservations.filter(is_public=True)

    return JsonResponse({
        'rooms': [
            {'id': r.slug, 'title': r.name,
             'eventColor': r.color}
            for r in Room.objects.all()
        ],
        'reservations': [
            {'id': r.pk, 'resourceId': r.room.slug, 'title': r.title,
             'start': r.start, 'end': r.end}
            for r in reservations
        ]
    })
