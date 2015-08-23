"""Classes and enumerations related to the management of the organisation.

This exports:
    - CASH: equals to 'cash'. Used in PAYMENT_MEANS enumeration.
    - CHEQUE: equals to 'cheque'. Used in PAYMENT_MEANS enumeration.
    - PAYMENT_MEANS: enumeration for payment means (CASH or CHEQUE).
    - CERTIFICATE_VALIDITY: equals to 52 (weeks). Used to compute validity of the
        certificate.
    - DELTA_CERTIFICATE_VALIDITY: equals to 6 (weeks). Used to allow certificates
        older by less than DELTA_CERTIFICATE_VALIDITY weeks more than
        CERTIFICATE_VALIDITY.

    - Weekday: class representing a weekday in Django format.
    - Location: class representing a location.
    - Lending: class representing a lending of an equipment.
    - Equipment: class representing equipment.
    - Permanence: class representing the opening hours.
    - MembershipType: class representing all the different types of memberships.
    - Membership: class representing a membership for a user.
    - Position: class representing a position in the association (~ staff)
    - PublicFile: class representing a file accessible to all.
    - PublicImage: class representing a file accessible to all.
    - ProtectedFile: class representing a file accessible to registered members.
    - ProtectedImage: class representing a file accessible to register members.
    - AdminFile: class representing a file accessible to admin users (~ staff).
    - AdminImage: class representing a file accessible to admin users (~ staff).
"""
from django.db import models
from sorl.thumbnail import ImageField
from django.core.exceptions import ValidationError
from django.core.validators import (MaxValueValidator, MinValueValidator)
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from datetime import (timedelta, date)
from users.models import CustomUser
from treasury.models import CashRegister


class Weekday(object):
    """Model representing weekday in Django format.

    Django and python formats are different for weekdays. This class is an helper
    to avoid mistakes.

    https://docs.djangoproject.com/en/1.8/ref/models/querysets/#week-day
    https://docs.python.org/3.4/library/datetime.html#datetime.date.weekday

    Enumeration of integers:
        - WEEKDAYS: as in Django format. 1 for Sunday, 7 for Saturday.

    Methods:
        - to_date_weekday: transform a django weekday into a date weekday.
        - to_django_weekday: transform a date weekday into a django weekday.
    """

    WEEKDAYS = (
        (1, _('Sunday')),
        (2, _('Monday')),
        (3, _('Tuesday')),
        (4, _('Wednesday')),
        (5, _('Thursday')),
        (6, _('Friday')),
        (7, _('Saturday'))
    )

    def to_date_weekday(django_weekday):
        """Transform a django weekday into a date weekday."""

        if django_weekday-2 < 0:
            return 6
        return django_weekday-2

    def to_django_weekday(date_weekday):
        """Transform a date weekday into a django weekday."""
        if date_weekday+2 > 7:
            return 1
        return date_weekday+2

CASH = 'cash'
CHEQUE = 'cheque'

PAYMENT_MEANS = (
    (CASH, _('Cash')),
    (CHEQUE, _('Cheque'))
)

CERTIFICATE_VALIDITY = 52
DELTA_CERTIFICATE_VALIDITY = 6


class Location(models.Model):
    """Model representing a location.

    A location can be defined by an address and a city or a latitude and a
    longitude.

    Attributes:
        - address: string storing the address (without the city) of the location.
            Can be None.
        - city: string storing the city of the location. Can be None.
        - latitude: float representing the latitude of the location. Can be None.
        - longitude: float representing the latitude of the longitude. Can be
            None.
        - name: string storing the name of the location.

    Relationships with other models:
        - activities: several activities taking place in this location.
        - matches: several matches taking place in this location.
        - permanences: several permanences taking place in this location.
        - sessions: several sessions taking place in this location.

    Ordering by ASCending name.

    Clean:
        - latitude and longitude has to be both either set or omitted.
        - address cannot be set without the city.
        - at least city should be set if latitude and longitude are omitted.
    """

    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=30, blank=True)
    latitude = models.FloatField(default=None, null=True, blank=True,
                validators = [MaxValueValidator(90), MinValueValidator(0)])
    longitude = models.FloatField(default=None, null=True, blank=True,
                validators = [MaxValueValidator(180), MinValueValidator(-180)])
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')
        ordering = ['name']

    def clean(self):
        print(self.latitude, self.longitude, self.address, self.city)
        if (self.latitude is not None and self.longitude is None) or\
                (self.latitude is None and self.longitude is not None):
            raise ValidationError(_('Latitude and longitude have to be both \
                                    either omitted or set.'))
        if self.address and not self.city:
            raise ValidationError(_('Address cannot be set without a city.'))
        if self.latitude is None and self.longitude is None and\
                not self.address and not self.city:
            raise ValidationError(_('Missing address and city or latitude and \
                                    longitude'))


class Permanence(models.Model):
    """Model representing a permanence.

    A permanence is a date or an interval of several hours representing the
    opening days or hours of the office. It can be on a weekly basis or
    occasional.

    Attributes:
        - date: date of the occasional permanence. Can be None.
        - end_time: time of the end of the permanence.
        - start_time: time of the beginning of the permanence.
        - weekday: value of Weekday enumeration representing a permanence on a
            weekly basis. Can be None.

    Relationships with other models:
        - related_activities: several activities associated to this permanence.

    Clean:
        - weekday and date cannot be both set.
        - weekday or date has to be set.
        - start_time cannot be after end_date.
    """

    date = models.DateField(null=True, blank=True)
    end_time = models.TimeField()
    start_time = models.TimeField()
    weekday = models.PositiveSmallIntegerField(choices=Weekday.WEEKDAYS,
                null=True, blank=True)

    related_activities = models.ManyToManyField('activities.Activity',
                            related_name='permanences', blank=True,
                            limit_choices_to={'start_date__gt': timezone.now})

    class Meta:
        verbose_name = _('permanence')
        verbose_name_plural = _('permanences')

    def clean(self):
        if self.weekday is not None and self.date is not None:
            raise ValidationError(_('Weekday and date cannot be both set.'))
        if self.weekday is None and self.date is None:
            raise ValidationError(_('Weekday or date has to be set.'))
        if self.start_time >= self.end_time:
            raise ValidationError(_('Start time cannot be after end time.'))


class Equipment(models.Model):
    """Model representing an equipment.

    Attributes:
        - description: string storing the description of the equipment. Can be
            None.
        - name: string storing the name of the equipment.
        - quantity: integer representing the quantity in stock for this equipment.

    Relationships with other models:
        - lendings: several lendings associated to this equipment.

    Ordering by ASCending name.
    """

    description = models.TextField(blank=True)
    name = models.CharField(max_length=30, db_index=True)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),])

    class Meta:
        verbose_name = _('equipment')
        verbose_name_plural = _('equipments')
        ordering = ['name']


class Lending(models.Model):
    """Model representing a lending of an equipment.

    A lending is accepted only to registered users.

    Attributes:
        - deposit: integer representing the value of the deposit for this lending.
        - end_date: date of the supposed end of the lending.
        - quantity: integer representing the quantity of equipment lent.
        - returned: boolean indicating if the lending has been returned.
        - start_date: date of the beginning of the lending.

    Relationships with other models:
        - borrower: user associated to this lending.
        - equipment: equipment associated to this lending.

    Ordering by DESCending start_date.

    Clean:
        - start_date cannot be after end_date.
        - lent quantity cannot be superior to available stock for the equipment.
    """

    deposit = models.PositiveSmallIntegerField()
    end_date = models.DateField()
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),])
    returned = models.BooleanField(default=False)
    start_date = models.DateField(default=timezone.now)

    borrower = models.ForeignKey(CustomUser, related_name='lendings')
    equipment = models.ForeignKey(Equipment, related_name='lendings')

    class Meta:
        verbose_name = _('lending')
        verbose_name_plural = _('lendings')
        ordering = ['-start_date']

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError(_('Start date cannot be after end date.'))
        number_current_lendings = Lending.objects.filter(equipment=self.equipment,\
                                    returned=False).exclude(id__exact=self.id)\
                                    .aggregate(models.Sum('quantity'))\
                                    ['quantity__sum']
        if (number_current_lendings is not None and\
                number_current_lendings >= self.equipment.\
                quantity - self.quantity) or (number_current_lendings is None and\
                self.quantity > self.equipment.quantity):
            raise ValidationError(_('Lending impossible, not enough equipment \
                                    in stock.'))


class Position(models.Model):
    """Model representing a position in the association (~ staff).

    Attributes:
        - description: string storing the description of the position. Typically
            rights and duties.
        - title: string storing the title of the position.

    Relationships with other models:
        - vacant_positions: several vacant positions associated to this position.
        - users: several users occupying this position.
    """

    description = models.TextField()
    title = models.CharField(max_length=30)

    class Meta:
        verbose_name = _('position')
        verbose_name_plural = _('positions')


class MembershipType(models.Model):
    """Type of membership.

    A type of membership can be used to define different categories of users
    which can be used to sort users, apply a different price for different
    categories.

    A membership type should not be deleted since it can be useful for statistics.
    Instead, mark the unused one as is_active False.

    Attributes:
        - description: string storing the description of the membership type.
            Typically the requirements for fitting in the categorie of users.
        - is_active: boolean indicating if the membership type is usable or
            is stored only as a mean for archiving.
        - semester_fee: float storing the membership fees of this type for one
            semester.
        - title: string storing the title of the membership type.
        - year_fee: float storing the membership fees of this type for one year.

    Relationships with other models:
        - memberships: several memberships associated to this membership type.

    Ordering by ASCending semester_fee.
    """

    description = models.TextField()
    is_active = models.BooleanField(default=True)
    semester_fee = models.DecimalField(max_digits=6, decimal_places=2,
                    validators=[MinValueValidator(0),])
    title = models.CharField(max_length=30)
    year_fee = models.DecimalField(max_digits=6, decimal_places=2,
                validators=[MinValueValidator(0),])

    class Meta:
        verbose_name = _('membership type')
        verbose_name_plural = _('membership types')
        ordering = ['semester_fee']


class Membership(models.Model):
    """Model representing a membership for a user.

    A user can have several memberships used as a history for statistics.

    Attributes:
        - certificate: image being a copy of the certificate. Can be None if the
            certificate is included in membership_copy.
        - certificate_date: date of the issue of the certificate.
        - cheque_bank: string storing the name of the bank. Can be None if the
            participant did not pay with cheque.
        - creation_date: datetime of the creation of the participant. Not editable.
        - expiration_date: date of the expiration of the membership.
        - membership_copy: image being a copy of the membership paper.
        - payment_mean: string storing the payment mean. (see PAYMENT_MEANS)

    Relationships with other models:
        - member: user associated to this membership.
        - membership_type: the type of the membership.
        - cash_register: cash register associated to this membership.

    Ordering by DESCending expiration_date.

    Clean:
        - expiration_date cannot be after the creation_date.
        - if payment_mean is CHEQUE, the cheque_bank has to be set.
        - certificate has to be issued at maximum CERTIFICATE_VALIDITY +
            DELTA_CERTIFICATE_VALIDITY weeks before expiration_date.
    """
    certificate = ImageField(upload_to='admin/certificates', null=True,
                    blank=True)
    certificate_date = models.DateField()
    cheque_bank = models.CharField(max_length=30, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField()
    membership_copy = ImageField(upload_to='admin/memberships')
    payment_mean = models.CharField(max_length=6, choices=PAYMENT_MEANS)

    member = models.ForeignKey(CustomUser, related_name='membership_history')
    membership_type = models.ForeignKey(MembershipType, related_name='memberships',
                        limit_choices_to={'is_active': True}, null=True,
                        on_delete=models.SET_NULL)
    cash_register = models.ForeignKey(CashRegister, related_name='memberships',
                    on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _('membership')
        verbose_name_plural = _('memberships')
        ordering = ['-expiration_date']

    def clean(self):
        if (self.creation_date is not None and \
                self.expiration_date <= self.creation_date) or \
                (self.creation_date is None and self.expiration_date <=\
                date.today()):
            raise ValidationError(_('Expiration date cannot be after the creation\
                                    date.'))

        if self.payment_mean == CHEQUE and not self.cheque_bank:
            raise ValidationError(_('Missing bank of the cheque.'))
        if self.certificate_date + timedelta(weeks=CERTIFICATE_VALIDITY+\
                DELTA_CERTIFICATE_VALIDITY) <= self.expiration_date:
             raise ValidationError(_('Certificate will expire before the \
                                    membership.'))

# TODO: Migrate to generic many-to-many relation?
# http://stackoverflow.com/questions/933092/generic-many-to-many-relationships

class PublicFile(models.Model):
    """File accesible to unregistered users.

    Files are stored in public/files/ or public/weekmail for Weekmail attached
    files.

    Attributes:
        - creation_date: datetime of the creation of the file. Not editable.
        - file: the uploaded file.

    Relationships with other models:
        - Generic Relation.

    Ordering by DESCending creation_date.
    """

    def custom_path(instance, filename):
        directory = 'files/'
        if str(instance.content_type) == "weekmail":
            directory = 'weekmail/%s/%s' % (instance.object_id, filename)
        return 'public/%s%s' % (directory, filename)

    creation_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=custom_path)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-creation_date']


class PublicImage(models.Model):
    """Image accesible to unregistered users.

    Images are stored in public/images/.

    Attributes:
        - creation_date: datetime of the creation of the image. Not editable.
        - file: the uploaded image.

    Relationships with other models:
        - Generic Relation.

    Ordering by DESCending creation_date.
    """

    def custom_path(instance, filename):
        directory = ''
        return 'public/images/%s%s' % (directory, filename)

    creation_date = models.DateTimeField(auto_now_add=True)
    file = ImageField(upload_to=custom_path)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-creation_date']


class ProtectedFile(models.Model):
    """File accesible to registered users.

    Files are stored in protected/ or:
        - protected/activities/[activity.id]/ for Activity attached files.
        - protected/articles/[article.id]/ for Article attached files.

    Attributes:
        - creation_date: datetime of the creation of the file. Not editable.
        - file: the uploaded file.

    Relationships with other models:
        - Generic Relation.

    Ordering by DESCending creation_date.
    """

    def custom_path(instance, filename):
        directory = ''
        if str(instance.content_type) == "activity":
            directory = 'activities/%s/' % (instance.object_id)
        if str(instance.content_type) == "article":
            directory = 'articles/%s/' % (instance.object_id)
        return 'protected/%s%s' % (directory, filename)

    creation_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=custom_path)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-creation_date']


class ProtectedImage(models.Model):
    """Image accesible to registered users.

    Images are stored in protected/ or:
        - protected/activities/[activity.id]/ for Activity attached images.
        - protected/articles/[article.id]/ for Article attached images.
        - protected/matches/[match.id]/ for Match attached images.

    Attributes:
        - creation_date: datetime of the creation of the image. Not editable.
        - file: the uploaded image.

    Relationships with other models:
        - Generic Relation.

    Ordering by DESCending creation_date.
    """

    def custom_path(instance, filename):
        directory = ''
        if str(instance.content_type) == "activity":
            directory = 'activities/%s/' % (instance.object_id)
        if str(instance.content_type) == "article":
            directory = 'articles/%s/' % (instance.object_id)
        if str(instance.content_type) == "match":
            directory = 'matches/%s/' % (instance.object_id)
        return 'protected/%s%s' % (directory, filename)

    creation_date = models.DateTimeField(auto_now_add=True)
    file = ImageField(upload_to=custom_path)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-creation_date']


class AdminFile(models.Model):
    """File accesible to admin users (~ staff).

    Files are stored in admin/ or:
        - admin/activities/[activity.id]/ for Activity attached files.
        - admin/finances/[article.id]/ for FinancialOperation attached files.

    Attributes:
        - creation_date: datetime of the creation of the file. Not editable.
        - file: the uploaded file.

    Relationships with other models:
        - Generic Relation.

    Ordering by DESCending creation_date.
    """

    def custom_path(instance, filename):
        directory = ''
        if str(instance.content_type) == "activity":
            directory = 'activities/%s/' % (instance.object_id)
        if str(instance.content_type) == "financialoperation":
            directory = 'finances/%s/' % (instance.object_id)
        return 'admin/%s%s' % (directory, filename)

    creation_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=custom_path)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-creation_date']


class AdminImage(models.Model):
    """Image accesible to admin users (~ staff).

    Images are stored in admin/.

    Attributes:
        - creation_date: datetime of the creation of the image. Not editable.
        - file: the uploaded image.

    Relationships with other models:
        - Generic Relation.

    Ordering by DESCending creation_date.
    """

    def custom_path(instance, filename):
        directory = ''
        return 'admin/%s%s' % (directory, filename)

    creation_date = models.DateTimeField(auto_now_add=True)
    file = ImageField(upload_to=custom_path)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-creation_date']
