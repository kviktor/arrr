from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import (
    ModelForm, EmailField, DateTimeField, ValidationError, CharField)
from django.utils.translation import ugettext_lazy as _

from .models import Room, Reservation


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ("name", "description", )


class UserRegisterForm(UserCreationForm):
    email = EmailField(label=_("Email"))
    first_name = CharField()
    last_name = CharField()

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", )


class ReservationForm(ModelForm):
    start = DateTimeField()
    end = DateTimeField()

    class Meta:
        model = Reservation
        fields = ("title", "room", "start", "end", "is_public", )

    def clean_start(self):
        start = self.cleaned_data['start']
        room = self.cleaned_data.get("room")

        if not room:
            return

        reservation = Reservation.objects.filter(
            room=room, status="a", start__lte=start, end__gte=start).first()
        if reservation and self.instance != reservation:
            raise ValidationError(
                _("The start date overlaps with an already approved "
                  "reservation."))

        return start

    def clean_end(self):
        end = self.cleaned_data['end']
        room = self.cleaned_data.get("room")

        if not room:
            return

        reservation = Reservation.objects.filter(
            room=room, status="a", start__lte=end, end__gte=end).first()
        if reservation and self.instance != reservation:
            raise ValidationError(
                _("The end date overlaps with an already approved "
                  "reservation."))

        return end

    def clean(self):
        data = super().clean()
        start = data.get("start")
        end = data.get("end")
        room = data.get("room")

        if not (start and end and room):
            return data

        if end < start:
            raise ValidationError(
                _("End date must be later than start date."))

        rsv = Reservation.objects.filter(
            room=room, status="a", start__lte=start, end__gte=end).first()
        if rsv and rsv != self.instance:
            raise ValidationError(_("The given dates overlap with the "
                                    "timeline of another reservation for "
                                    "this room."))
