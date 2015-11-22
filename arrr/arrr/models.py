from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import BooleanField, ForeignKey, TextField, CharField

from autoslug import AutoSlugField
from model_utils.models import TimeFramedModel, TimeStampedModel


class Room(TimeStampedModel):
    slug = AutoSlugField(unique=True, populate_from="name", always_update=True)
    name = CharField(unique=True, max_length=50)
    description = TextField(blank=True)
    creator = ForeignKey(User, related_name='created_rooms')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("room-detail", kwargs={'slug': self.slug})


class Reservation(TimeFramedModel):
    title = TextField()
    is_public = BooleanField(default=False)
    room = ForeignKey(Room)
    reserver = ForeignKey(User, related_name='reservations')

    def get_absolute_url(self):
        return reverse("reservation-detail", kwargs={'pk': self.pk})
