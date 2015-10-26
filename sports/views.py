from django.shortcuts import get_object_or_404, render
from django.views.generic import (View, ListView)
from .models import Sport
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.http import (HttpResponseRedirect, HttpResponsePermanentRedirect,
                        HttpResponse, Http404)

class OverviewView(View):
    template_name = 'sports/sport_list.html'

    def get(self, request):
        open_sports = Sport.objects.filter(is_open=True)
        closed_sports = Sport.objects.filter(is_open=False)
        content = {'open_sports':open_sports, 'closed_sports':closed_sports}
        return render(request, self.template_name, content)

    def post(self, request):
        return HttpResponseRedirect(reverse('sports:overview'))

class DetailView(View):
    template_name = 'sports/sport.html'

    def get(self, request, pk, slug=None):
        sport = get_object_or_404(Sport, pk=pk)
        content = {'sport':sport}
        if sport.slug != slug:
            return HttpResponsePermanentRedirect(reverse('sports:sport',
                kwargs={'pk':pk, 'slug':sport.slug}))
        return render(request, self.template_name, content)

    def post(self, request):
        return HttpResponseRedirect(reverse('sports:sport',
            kwargs={'pk':pk, 'slug':sport.slug}))
