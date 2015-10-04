from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from activities.models import Activity
from communication.models import Article
from sports.models import (Session, Match)
from management.models import Weekday
from datetime import (datetime, timedelta)
from django.http import (HttpResponseRedirect, HttpResponse)

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
            'match': {'is_past': is_past, 'object': match},}
        print(content)
        return render(request, self.template_name, content)

    def post(self, request):
        return HttpResponseRedirect('home')
