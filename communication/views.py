from django.shortcuts import get_object_or_404, render
from django.views.generic import (View, ListView)
from django.utils.translation import ugettext as _
from django.db.models import Q
from activities.models import Activity
from communication.models import (Article, Information, Weekmail)
from sports.models import (Session, Match)
from management.models import Weekday
from datetime import (datetime, timedelta)
from django.utils import timezone
from django.http import (HttpResponseRedirect, HttpResponsePermanentRedirect,
                        HttpResponse, Http404)
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain

class HomeView(View):
    template_name = 'communication/home.html'

    def get(self, request):
        now = datetime.now()
        nowWeekday = Weekday.to_django_weekday(now.weekday())
        activities = Activity.objects.exclude(publication_date__gt=now).\
            exclude(end_date__lt=now).exclude(publication_date__isnull=True).\
            filter(is_frontpage=True).order_by('-publication_date')
        articles = Article.objects.exclude(publication_date__gt=now).\
            exclude(publication_date__isnull=True).filter(is_frontpage=True).\
            order_by('-publication_date')
        sessions = Session.objects.filter(sport__is_open=True).\
            filter(Q(weekday=nowWeekday) | Q(weekday=(nowWeekday+1)%7) | Q(weekday=(nowWeekday+2)%7) ).\
            order_by('weekday').order_by('start_time')
        informations = Information.objects.filter(is_important=True, is_published=True).\
            filter(Q(start_date__lt=now) | Q(start_date__isnull=True)).\
            filter(Q(end_date__gt=now) | Q(end_date__isnull=True)).\
            order_by('-end_date')
        is_past = False
        match = Match.objects.filter(date__gt=now).order_by('date').first()
        if not match:
            match = Match.objects.filter(date__lt=now).order_by('-date').first()
            is_past = True
        days = [now,now+timedelta(1),now+timedelta(2)]
        weekdays = [Weekday.to_django_weekday(day.weekday()) for day in days]
        content = {'activities': activities, 'articles': articles,
            'num_frontpage': range(activities.count() + articles.count()),
            'days_sessionsPerDay': zip(days,
                [sessions.filter(weekday=weekday) for weekday in weekdays]),
            'match': {'is_past': is_past, 'object': match},
            'informations': informations}
        return render(request, self.template_name, content)

    def post(self, request):
        return HttpResponseRedirect('home')

def returnDate(instance):
    if instance.__class__.__name__ == 'Weekmail':
        return instance.sent_date
    return instance.publication_date

class NewsView(View):
    template_name = "communication/news.html"

    def get(self, request):
        now = datetime.now()
        articles_list = Article.objects.exclude(publication_date__gt=now).\
            exclude(publication_date__isnull=True).order_by('-publication_date')
        weekmails_list = Weekmail.objects.exclude(sent_date__gt=now).\
            exclude(sent_date__isnull=True).order_by('-sent_date')
        news_list = sorted(chain(articles_list, weekmails_list), key=returnDate, reverse=True)

        paginator = Paginator(news_list, 9)
        page = request.GET.get('page')

        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'news': news,})

    def post(self, request):
        return HttpResponseRedirect('communication:news')

class ArticlesView(ListView):
    model = Article
    paginate_by = 9

    def get_queryset(self):
        now = datetime.now()
        return Article.objects.exclude(publication_date__gt=now).\
            exclude(publication_date__isnull=True).order_by('-publication_date')

class ArticleView(View):
    template_name = "communication/article.html"

    def get(self, request, pk, slug=None):
        article = get_object_or_404(Article, pk=pk)
        content = {'article': article,}
        now = timezone.now()
        if not article.publication_date or article.publication_date > now:
            raise Http404(_("Article does not exist."))
        if article.slug != slug:
            return HttpResponsePermanentRedirect(reverse('communication:article',
                kwargs={'pk':pk, 'slug':article.slug}))
        return render(request, self.template_name, content)

    def post(self, request):
        return HttpResponseRedirect('communication:article')

class WeekmailsView(ListView):
    model = Weekmail
    paginate_by = 9

    def get_queryset(self):
        now = datetime.now()
        return Weekmail.objects.exclude(sent_date__gt=now).\
            exclude(sent_date__isnull=True).order_by('-sent_date')

class WeekmailView(View):
    template_name = "communication/weekmail_display.html"

    def get(self, request, pk):
        weekmail = get_object_or_404(Weekmail, pk=pk)
        content = {'weekmail': weekmail,}
        now = timezone.now()
        if not weekmail.sent_date or weekmail.sent_date > now:
            raise Http404(_("Weekmail does not exist."))
        return render(request, self.template_name, content)

    def post(self, request):
        return HttpResponseRedirect('communication:weekmail')
