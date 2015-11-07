from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from .views import home

urlpatterns = patterns(
    '',
    url(r'^$', lambda x: redirect(reverse("home"))),
    url(r'^home/$', home, name="home"),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
