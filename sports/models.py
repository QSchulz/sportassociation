from django.db import models
from django.utils.translation import ugettext as _
from django.utils import timezone
from datetime import (timedelta, date)
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from users.models import CustomUser
from management.models import (Location, ProtectedImage, Weekday)
from communication.models import Article


class Sport(models.Model):
    """Model representing a sport.

    Attributes:
        - creation_date: datetime of the creation of the sport. Not editable.
        - description: string storing the description of the sport. Can be None.
        - is_open: boolean indicating if the sport can be practiced.
        - mailing_list: string storing the email representing the mailing list
            used to communicate with all participants of this sport. Can be None.
        - modification_date: datetime of the last modification of the sport.
            Not editable.
        - name: string storing the name of the sport.
        - slug: string only used for SEO.

    Relationships with other models:
        - competitors: several members engaged in competition in this sport.
        - managers: several members who manage the sport.
        - matches: several matches associated to this sport.
        - participants: several members who attend the sport or want to be
            informed of news in this sport.
        - sessions: several sessions associated to this article. Typically, the
            article will give report on these games.

    Ordering by ASCending name.
    """

    creation_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    is_open = models.BooleanField(default=True)
    mailing_list = models.EmailField(blank=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    competitors = models.ManyToManyField(CustomUser, blank=True,
                    related_name='competition_sports')
    managers = models.ManyToManyField(CustomUser, related_name='managed_sports')
    participants = models.ManyToManyField(CustomUser, blank=True,
                    related_name='subscribed_sports')

    class Meta:
        verbose_name = _('sport')
        verbose_name_plural = _('sports')
        ordering = ['name']

    def __str__(self):
        return '%s' % (self.name)

    # TODO: Validate manager is a member in forms


class Match(models.Model):
    """Model representing a match.

    Attributes:
        - date: datetime of the beginning of the match.
        - description: string storing the description of the match (Typically
            trip tips, teaser, context of the match...).
        - name: string storing the "name" of the match.
        - opponent: string storing the name of the opposing player/team.
        - result: string storing the result of the match.

    Relationships with other models:
        - attached_photos: several photos destined to registered users taken
            during the match.
        - location: location associated to the match.
        - report: article associated to the match.
        - sport: sport associated to the match.

    Ordering by DESCending date.
    """

    date = models.DateTimeField()
    description = models.TextField()
    name = models.CharField(max_length=50)
    opponent = models.CharField(max_length=30, blank=True)
    result = models.CharField(max_length=50, blank=True)

    attached_photos = GenericRelation(ProtectedImage, blank=True)
    location = models.ForeignKey(Location, related_name='matches', null=True,
                blank=True, on_delete=models.SET_NULL)
    report = models.ForeignKey(Article, related_name="matches", null=True,
                blank=True, on_delete=models.SET_NULL)
    sport = models.ForeignKey(Sport, related_name='matches', null=True,
            blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('match')
        verbose_name_plural = _('matches')
        ordering = ['-date']

    def __str__(self):
        return '%s (%s)' % (self.name, str(self.date))


class Session(models.Model):
    """Session associated to a sport.

    A session can be organised weekly but also occasionally.

    Attributes:
        - date: date of the occasional session.
        - end_time: time of the end of the session.
        - start_time: time of the beginning of the session.
        - weekday: day of the week of the weekly session.

    Relationships with other models:
        - cancelled_sessions: several cancelled sessions associated to this session.
        - location: location associated to this session.
        - manager: member who is in charge of this session.
        - sport: sport associated to this session.

    Ordering by ASCending weekday.

    Clean:
        - one of weekday or date has to be set.
        - weekday and date cannot be both set.
        - start_time cannot be after end_date.
        - only a member registered as a manager of the sport can manage the session.
    """

    date = models.DateField(default=None, null=True, blank=True)
    end_time = models.TimeField()
    start_time = models.TimeField()
    weekday = models.PositiveSmallIntegerField(choices=Weekday.WEEKDAYS, null=True,
                blank=True)

    #def _limit_choices_manager():
    #    return models.Q(managed_sports__isnull=False)

    location = models.ForeignKey(Location, related_name='sessions',
                on_delete=models.SET_NULL, null=True)
    manager = models.ForeignKey(CustomUser, related_name='managed_sessions',
                on_delete=models.SET_NULL, null=True)#,
                #limit_choices_to=_limit_choices_manager)
    sport = models.ForeignKey(Sport, related_name='sessions',
            limit_choices_to={'is_open': True})

    class Meta:
        verbose_name = _('session')
        verbose_name_plural = _('sessions')
        ordering = ['weekday']

    def clean(self):
        if self.weekday is not None and self.date is not None:
            raise ValidationError(_('Weekday and date cannot be both set.'))
        if self.weekday is None and self.date is None:
            raise ValidationError(_('Weekday or date has to be set.'))
        if self.start_time >= self.end_time:
            raise ValidationError(_('Start time cannot be after end time.'))
        if not self.sport in self.manager.managed_sports.all():
            raise ValidationError(_('%s does not manage the sport. (S)he can\'t \
                                    manage sessions of this sport.' % \
                                    (self.manager.user.get_full_name())))

    def __str__(self):
        return '%s (%s)' % (self.sport.name, str(self.date) if self.weekday is \
            None else self.get_weekday_display())


class CancelledSession(models.Model):
    """Cancelled session associated to session.

    Attributes:
        - cancellation_date: date of the cancelled session.
        - description: string storing the description of the cancelled session.
            Typically the reason of the cancellation. Can be None.
        - title: string storing the title of the cancelled session. Typically a
            short description of the reason of cancellation.

    Relationships with other models:
        - cancelled_session: several files destined to registered users.

    Ordering by ASCending cancellation_date.

    Clean:
        - if the cancelled session is organised weekly, weekdays have to match.
        - else, dates have to match.
    """

    cancellation_date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True)
    title = models.CharField(max_length=50)

    cancelled_session = models.ForeignKey(Session,
                        related_name='cancelled_sessions')

    class Meta:
        verbose_name = _('cancelled session')
        verbose_name_plural = _('cancelled sessions')
        ordering = ['cancellation_date']

    def clean(self):
        if self.cancelled_session.weekday is not None and\
                Weekday.to_django_weekday(self.cancellation_date.weekday())\
                != self.cancelled_session.weekday:
            raise ValidationError(_('Weekdays are not matching.'))
        if self.cancelled_session.weekday is None and\
                self.cancellation_date != self.cancelled_session.date:
            raise ValidationError(_('Dates are not matching.'))

    def __str__(self):
        return '%s (%s)' % (self.cancelled_session.sport,
            str(self.cancellation_date))
