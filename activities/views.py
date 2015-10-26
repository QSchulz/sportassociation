from django.shortcuts import get_object_or_404, render
from django.views.generic import (View, ListView)
from activities.models import Activity
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.http import (HttpResponseRedirect, HttpResponsePermanentRedirect,
                        HttpResponse, Http404)

class OverviewView(ListView):
    model = Activity
    paginate_by = 9

    def get_queryset(self):
        now = timezone.now()
        activities = Activity.objects.exclude(publication_date__gt=now).\
            exclude(publication_date__isnull=True).\
            order_by('-publication_date')
        return activities


class BigActivitiesView(ListView):
    model = Activity
    template_name = 'activities/activity_list.html'
    paginate_by = 9

    def get_queryset(self):
        now = timezone.now()
        activities = Activity.objects.exclude(publication_date__gt=now).\
            exclude(publication_date__isnull=True).filter(is_big_activity=True).\
            order_by('-publication_date')
        return activities

class ActivitiesView(ListView):
    model = Activity
    template_name = 'activities/activity_list.html'
    paginate_by = 9

    def get_queryset(self):
        now = timezone.now()
        activities = Activity.objects.exclude(publication_date__gt=now).\
            exclude(publication_date__isnull=True).filter(is_big_activity=False).\
            order_by('-publication_date')
        return activities

class DetailView(View):
    template_name = 'activities/activity.html'

    def get(self, request, pk, slug=None):
        activity = get_object_or_404(Activity, pk=pk)
        content = {'activity':activity}
        now = timezone.now()
        if not activity.publication_date or activity.publication_date > now:
            raise Http404(_("Activity does not exist."))
        if activity.slug != slug:
            return HttpResponsePermanentRedirect(reverse('activities:activity',
                kwargs={'pk':pk, 'slug':activity.slug}))
        return render(request, self.template_name, content)

    def post(self, request):
        return HttpResponseRedirect(reverse('activities:activity',
            kwargs={'pk':pk, 'slug':activity.slug}))
