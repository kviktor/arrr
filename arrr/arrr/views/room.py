from django.core.urlresolvers import reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)


from braces.views import LoginRequiredMixin
from braces.views import StaffuserRequiredMixin

from ..models import Room
from ..forms import RoomForm


class RoomListView(ListView):
    model = Room
    template_name = "room/list.html"


class RoomCreateView(LoginRequiredMixin, StaffuserRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = "room/create.html"

    def form_valid(self, form):
        room = form.save(commit=False)
        room.creator = self.request.user
        return super().form_valid(form)


class RoomDetailView(DetailView):
    model = Room
    template_name = "room/detail.html"
    slug_field = "slug"
    slug_url_kwars = "slug"


class RoomEditView(LoginRequiredMixin, StaffuserRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = "room/edit.html"
    slug_field = "slug"
    slug_url_kwars = "slug"


class RoomDeleteView(LoginRequiredMixin, StaffuserRequiredMixin, DeleteView):
    model = Room
    template_name = "base-delete.html"
    slug_field = "slug"
    slug_url_kwars = "slug"

    def get_success_url(self):
        return reverse("room.list")
