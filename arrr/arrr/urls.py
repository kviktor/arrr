from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from .views import (
    home,
    RoomCreateView, RoomDetailView, RoomListView, RoomEditView, RoomDeleteView,
    UserRegisterView,
    ReservationCreateView, ReservationDetailView, ReservationListView,
    ReservationEditView, ReservationDeleteView,
)

urlpatterns = patterns(
    '',
    url(r'^$', lambda x: redirect(reverse("home"))),
    url(r'^home/$', home, name="home"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^room/create/$', RoomCreateView.as_view(), name="room.create"),
    url(r'^room/list/$', RoomListView.as_view(), name="room.list"),
    url(r'^room/(?P<slug>[A-Za-z0-9\-]+)/$',
        RoomDetailView.as_view(), name="room.detail"),
    url(r'^room/(?P<slug>[A-Za-z0-9\-]+)/edit/$',
        RoomEditView.as_view(), name="room.edit"),
    url(r'^room/(?P<slug>[A-Za-z0-9\-]+)/delete/$',
        RoomDeleteView.as_view(), name="room.delete"),

    url(r'^reservation/create/$', ReservationCreateView.as_view(),
        name="reservation.create"),
    url(r'^reservation/list/$', ReservationListView.as_view(),
        name="reservation.list"),
    url(r'^reservation/(?P<pk>\d+)/$',
        ReservationDetailView.as_view(), name="reservation.detail"),
    url(r'^reservation/(?P<pk>\d+)/edit/$',
        ReservationEditView.as_view(), name="reservation.edit"),
    url(r'^reservation/(?P<pk>\d+)/delete/$',
        ReservationDeleteView.as_view(), name="reservation.delete"),

    url('^register/$', UserRegisterView.as_view(), name="register"),
    url('^', include('django.contrib.auth.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
