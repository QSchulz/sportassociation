from django.db import models
from sorl.thumbnail import ImageField
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib.contenttypes.fields import GenericRelation
from management.models import (Location, PAYMENT_MEANS, ProtectedImage,
                                ProtectedFile, AdminFile, CHEQUE)
from users.models import CustomUser
from treasury.models import CashRegister


class Activity(models.Model):
    """Model representing an activity.

    Attributes:
        - content: string storing the description of the activity
        - cover: image illustrating the activity. Can be None.
        - creation_date: datetime of the creation of the activity. Not editable.
        - end_date: datetime of the end of the activity.
        - is_big_activity: boolean to differientate "big" activities from normal
            ones.
        - is_frontpage: boolean indicating if the activity should be displayed on
            the front-page.
        - is_member_only: boolean indicating if the activity is reserved to members.
        - modification_date: datetime of the last modification of the activity.
            Not editable.
        - publication_date: datetime of the publication of the activity. Can be
            "in the future". Can be None ("draft" mode).
        - slug: string only used for SEO.
        - start_date: datetime of the beginning of the activity.
        - summary: string storing the summary of the activity used when displaying
            activities in compact mode. Can be None.
        - title: string storing the title of the activity.
        - website: string storing the full URL of the website associated to this
            activity. Can be None.

    Relationships with other models:
        - attached_admin_files: several files destined to admin staff only.
            Typically copies of letters, mails, estimates...
        - attached_files: several files destined to registered users. Typically
            reservation forms, information...
        - attached_photos: several photos associated to this activity destined to
            registered users.
        - financial_operations: several financial operations associated to this
            activity. Typically fees and subventions.
        - location: location of the activity.
        - parameters: several parameters associated to the activity.
        - permanences: several permanences to pay for the activity.

    Ordering by DESCending publication_date

    Clean:
        - start_date cannot be after end_date
    """

    content = models.TextField()
    cover = ImageField(upload_to='public/covers/activities/', null=True,
            blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_big_activity = models.BooleanField(default=False)
    is_frontpage = models.BooleanField(default=False, db_index=True)
    is_member_only = models.BooleanField(default=False)
    modification_date = models.DateTimeField(auto_now=True)
    publication_date = models.DateTimeField(db_index=True, null=True, blank=True)
    slug = models.SlugField()
    start_date = models.DateTimeField()
    summary = models.CharField(max_length=180, blank=True)
    title = models.CharField(max_length=50, db_index=True)
    website = models.URLField(blank=True)

    attached_admin_files = GenericRelation(AdminFile, blank=True)
    attached_files = GenericRelation(ProtectedFile, blank=True)
    attached_photos = GenericRelation(ProtectedImage, blank=True)
    location = models.ForeignKey(Location, related_name='activities', null=True,
                on_delete=models.SET_NULL, blank=True)

    class Meta:
        verbose_name = _('activity')
        verbose_name_plural = _('activities')
        ordering = ['-publication_date']

    def clean(self):
        if self.start_date is not None and self.end_date is not None and\
                self.start_date >= self.end_date:
            raise ValidationError(_('Start date cannot be after end date.'))

    def __str__(self):
        return '%s (%s %s)' % (self.title, self.start_date.month,
            self.start_date.year)


class Parameter(models.Model):
    """Parameter of an activity.

    A parameter of an activity represents a category of choices (see Item)
    for this activity. The choices are grouped in categories. A category can have
    subcategories, which may be mandatory when filling the form. A category can
    have a limited number of "places".
    A parameter can be "published" thus being displayed on activity's page.
    A parameter without a parent parameter is typically the admission to an
    activity and subcategories are parameters of this admission (typically player
    level...).

    Attributes:
        - creation_date: datetime of the creation of the parameter. Not editable.
        - default_price: float storing the default price.
        - description: string storing a description of the parameter. Can be None.
        - is_mandatory: boolean available only for parameters representing
            "subcategories" to tell they have to be mandatory filled when filling
            their parent. Typically, the buying of the parent cannot be done
            without the buying of the children parameters.
        - is_member_only: boolean indicating if it is reserved to members.
        - is_published: boolean indicating if this parameter should be displayed
            on activity's page publicly visible.
        - max_bought_items: integer storing the maximum number of all items
            available to buy.
        - member_price: float storing the price for members.
        - modification_date: datetime of the last modification of the parameter.
            Not editable.
        - name: string storing the name of the parameter.

    Relationships with other models:
        - activity: activity associated to the parameter.
        - associated_parameters: several parameters associated to this parameter
            as "subcategories".
        - items: several items associated to this parameter.
        - parent_parameter: parameter representing the parent parameter of this
            parameter.

    Ordering by ASCending creation_date.
    """

    creation_date = models.DateTimeField(auto_now_add=True)
    default_price = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                    validators = [MinValueValidator(0),])
    description = models.TextField(blank=True)
    is_mandatory = models.BooleanField(default=False)
    is_member_only = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    max_bought_items = models.PositiveSmallIntegerField(default=None, blank=True,
                        null=True)
    member_price = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                    validators = [MinValueValidator(0),])
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)

    activity = models.ForeignKey(Activity, related_name='parameters', blank=True,
                null=True)
    parent_parameter = models.ForeignKey('self', null=True, blank=True,
                        related_name='associated_parameters')

    class Meta:
        verbose_name = _('parameter')
        verbose_name_plural = _('parameters')
        ordering = ['creation_date']

    def clean(self):
        if self.activity is None and self.parent_parameter is None:
            raise ValidationError(_('Parent parameter or activity has to be set.'))

    def __str__(self):
        return '%s' % (self.name)


class Item(models.Model):
    """Item of a parameter.

    An item represents a choice among the choices available in a category (see
    Parameter). It can have its own maximal number of stocks available to buy, a
    specific default price and member price.

    Attributes:
        - creation_date: datetime of the creation of the item. Not editable.
        - description: string storing a description of the item. Can be None.
        - default_price: float storing the default price specific to this item.
        - max_bought_items: integer storing the maximum number of this item
            available to buy.
        - member_price: float storing the price for members specific to this item.
        - modification_date: datetime of the last modification of the item.
            Not editable.
        - name: string storing the name of the item.

    Relationships with other models:
        - parameter: parameter associated to this item.
        - participants: several participants associated to this item.

    Ordering by ASCending name.
    """

    creation_date = models.DateTimeField(auto_now_add=True)
    default_price = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                    validators = [MinValueValidator(0),])
    description = models.TextField(blank=True)
    max_bought_items = models.PositiveSmallIntegerField(default=None, null=True,
                        blank=True)
    member_price = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                    validators = [MinValueValidator(0),])
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)

    parameter = models.ForeignKey(Parameter, related_name='items')

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        ordering = ['name']

    def __str__(self):
        return '%s' % (self.name)


class Participant(models.Model):
    """Represent a bill of an item associated to one person.

    A participant can be identified by a member object or a name. To this bill is
    associated a payment mean and a cash register to archive it.

    Attributes:
        - creation_date: datetime of the creation of the participant. Not editable.
        - cheque_bank: string storing the name of the bank. Can be None if the
            participant did not pay with cheque.
        - modification_date: datetime of the last modification of the participant.
            Not editable.
        - payment_mean: string storing the payment mean. (see PAYMENT_MEANS)
        - unregistered_user: string storing the name of the user if (s)he is not
            a member.

    Relationships with other models:
        - cash_register: cash register associated to the payment of the participant.
        - item: item bought by the participant.
        - registered_user: user representing the participant.

    Ordering by ASCending registered_user and then by unregistered_user.

    Clean:
        - one of unregistered_user and registered_user has to be set.
        - unregistered_user and registered_user cannot both be set.
        - if payment_mean is CHEQUE, the cheque_bank has to be set.
        - unregistered members cannot buy a parameter reserved to members.
        - unregistered members cannot buy an activity reserved to members.
        - maximum number of participants for an item cannot be exceeded.
        - maximum number of participants for a parameter cannot be exceeded.
    """

    cheque_bank = models.CharField(max_length=30, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    payment_mean = models.CharField(max_length=6, choices=PAYMENT_MEANS)
    unregistered_user = models.CharField(max_length=30, null=True, blank=True)

    cash_register = models.ForeignKey(CashRegister, related_name='bought_items',
                    on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Item, related_name='participants')
    registered_user = models.ForeignKey(CustomUser, null=True, blank=True,
                        related_name='participations')

    class Meta:
        verbose_name = _('participant')
        verbose_name_plural = _('participants')
        ordering = ['registered_user', 'unregistered_user']

    def clean(self):
        if not self.unregistered_user and self.registered_user is None:
            raise ValidationError(_('One of unregistered user or registered user \
                                    should be set.'))
        if self.unregistered_user is not None and self.registered_user is not None:
            raise ValidationError(_('Maximum one of unregistered user or \
                                    registered user can be set.'))
        if self.payment_mean == CHEQUE and not self.cheque_bank:
            raise ValidationError(_('Missing bank of the cheque.'))
        # TODO: why checking None? It's a ForeignKey non-nullable.
        if self.item is None:
            return
        if self.unregistered_user is not None and \
                (self.item.parameter.is_member_only is True or \
                self.item.parameter.activity.is_member_only is True):
            raise ValidationError(_('Unregistered users cannot buy parameters \
                                    reserved to members or participate in \
                                    activity reserved to members.'))
        if Participant.objects.filter(item=self.item).count() >= self.item.\
                max_bought_items:
            raise ValidationError(_('Maximum number of bought items is reached \
                                    for this item.'))
        if Participant.objects.filter(item__parameter=self.item.parameter).\
                count() >= self.item.parameter.max_bought_items:
            raise ValidationError(_('Maximum number of bought items is reached \
                                    for this parameter.'))

    def __str__(self):
        return '%s (%s)' % (self.unregistered_user if not self.unregistered_user\
            else self.registered_user.user.get_full_name(), self.item.name)
