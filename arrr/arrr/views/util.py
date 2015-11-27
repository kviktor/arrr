from django.contrib.auth.models import User
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin

from ..models import Room, Reservation


class SearchView(LoginRequiredMixin, TemplateView):
    template_name = "util/search.html"

    def highlight(self, value, keyword):

        if not (value and keyword):
            return value

        try:
            idx = value.lower().index(keyword.lower())
            return mark_safe(
                escape(value[:idx]) +
                "<strong>" +
                escape(value[idx:idx + len(keyword)]) +
                "</strong>" +
                escape(value[idx + len(keyword):])
            )
        except ValueError:
            return value

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        searches = {
            Room: ["name", "description", ],
            Reservation: ["title", ],
            User: ["first_name", "last_name", ]
        }

        if self.request.user.is_staff:
            searches[User].append("email")

        results = {}
        keyword = self.request.GET.get("keyword")
        if keyword:
            for key, fields in searches.items():
                tmp = key.objects.none()
                for field in fields:
                    tmp = tmp | key.objects.filter(
                        **{'%s__icontains' % field: keyword})

                results[key.__name__] = tmp.distinct()
                for r in results[key.__name__]:
                    for f in fields:
                        setattr(r, f, self.highlight(getattr(r, f), keyword))

        ctx['results'] = results
        return ctx
