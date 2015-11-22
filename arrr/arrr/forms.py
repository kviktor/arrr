from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, EmailField
from django.utils.translation import ugettext_lazy as _

from .models import Room, Reservation


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ("name", "description", )


class UserRegisterForm(UserCreationForm):
    email = EmailField(label=_("Email"))

    class Meta:
        model = User
        fields = ("username", "email", )


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ("title", "room", "is_public", )
