from django.contrib.auth.models import User
from django.db.models import BooleanField, ForeignKey, TextField, CharField

from autoslug import AutoSlugField
from model_utils.models import TimeFramedModel, TimeStampedModel


class Room(TimeStampedModel):
    slug = AutoSlugField(populate_from="name")
    name = CharField(unique=True, max_length=50)
    description = TextField(blank=True)
    creator = ForeignKey(User, related_name='created_rooms')


class Reservation(TimeFramedModel):
    title = TextField()
    is_public = BooleanField(default=False)
    room = ForeignKey(Room)
    reserver = ForeignKey(User, related_name='reservations')
