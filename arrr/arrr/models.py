from hashlib import sha1

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import BooleanField, ForeignKey, TextField, CharField
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string

from autoslug import AutoSlugField
from model_utils.models import TimeFramedModel, TimeStampedModel


class Room(TimeStampedModel):
    slug = AutoSlugField(unique=True, populate_from="name", always_update=True)
    name = CharField(unique=True, max_length=50)
    description = TextField(blank=True)
    creator = ForeignKey(User, related_name='created_rooms')

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("room.detail", kwargs={'slug': self.slug})

    @property
    def color(self):
        return "#" + sha1(self.name.encode("utf-8")).hexdigest()[:6]


class Reservation(TimeFramedModel):
    STATUSES = (
        ('p', _("pending")),
        ('r', _("rejected")),
        ('a', _("approved"))
    )

    title = CharField(max_length=150)
    is_public = BooleanField(default=False)
    room = ForeignKey(Room)
    reserver = ForeignKey(User, related_name='reservations')
    status = CharField(max_length=1, choices=STATUSES, default="p")
    changed_by = ForeignKey(User, null=True)

    class Meta:
        ordering = ("start", )

    def get_absolute_url(self):
        return reverse("reservation.detail", kwargs={'pk': self.pk})


def send_notification(sender, instance, created, **kwargs):
    if not created:
       return

    message = render_to_string("email/reservation-notification.txt", {
        'reservation': instance, 'url': settings.DJANGO_URL.rstrip("/")
    })
    emails = User.objects.filter(is_staff=True).values_list("email", flat=True)

    send_mail("New reservation", message, settings.DEFAULT_FROM_EMAIL,
              emails, fail_silently=False)

post_save.connect(send_notification, sender=Reservation)
