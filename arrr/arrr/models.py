from django.contrib.auth.models import User
from django.db.models import BooleanField, ForeignKey, Model, TextField
from model_utils.models import TimeFramedModel


class Room(Model):
    name = TextField(unique=True)
    description = TextField(blank=True)
    creator = ForeignKey(User, related_name='created_rooms')


class Reservation(TimeFramedModel):
    title = TextField()
    is_public = BooleanField(default=False)
    room = ForeignKey(Room)
    reserver = ForeignKey(User, related_name='reservations')
