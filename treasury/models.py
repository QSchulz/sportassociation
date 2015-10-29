from django.db import models
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from users.models import CustomUser


class FinancialOperation(models.Model):
    """Model representing fees and subventions.

    A financial operation is a fee if its amount is negative or a subvention if
    it's positive. A fee can be paid by a user or an unregistered user while a
    subvention can be given by a user or an unregistered user. Files are attached
    for proof.
    A financial operation can be associated to an activity to keep track of its
    balance.

    Attributes:
        - amount: float representing the amount of the fee (has to be negative)
            or of the subvention.
        - creation_date: datetime of the creation of the fee or subvention.
            Not editable.
        - description: string storing the description of the fee or subvention.
            Typically the reason of such expense or under which constraints is
            given the subvention.
        - modification_date: datetime of the last modification of the fee or
            subvention. Not editable.
        - name: string storing the name of the fee or subvention to be easily
            found.
        - processed_date: datetime of the moment when the fee was paid back or
            the subvention received.
        - unregistered_user: string storing the name of the user who paid the fee
            or gave money if (s)he is not a member. Typically for organisations,
            companies...

    Relationships with other models:
        - files: several files destined to admin staff only as proof of payment
            or donation.
        - registered_user: user representing the user who paid the fee or gave
            money.
        - related_activity: activity associated to the fee or the subvention.

    Methods:
        - is_fee: return True if the amount of the financial operation is negative
        - is_subvention: return True if the amount of the financial operation is
            positive

    Ordering by DESCending creation_date.

    Clean:
        - one of unregistered_user and registered_user has to be set.
        - unregistered_user and registered_user cannot both be set.
    """

    amount = models.DecimalField(_('amount'), max_digits=8, decimal_places=2)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    description = models.TextField(_('description'))
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)
    name = models.CharField(_('name'), max_length=50)
    processed_date = models.DateField(_('processed date'), null=True, blank=True)
    unregistered_user = models.CharField(_('unregistered user'), max_length=50, blank=True)

    files = GenericRelation('management.AdminFile', blank=True, verbose_name=_('attached private files'))
    registered_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,
                        related_name='financial_operations', null=True, blank=True, verbose_name=_('registered user'))
    related_activity = models.ForeignKey('activities.Activity', null=True,
                        related_name='financial_operations', blank=True, verbose_name=_('related activity'))

    class Meta:
        verbose_name = _('financial operation')
        verbose_name_plural = _('financial operations')
        ordering = ['-creation_date']

    def is_fee(self):
        return amount < 0

    def is_subvention(self):
        return amount > 0

    def clean(self):
        if not self.unregistered_user and self.registered_user is None:
            raise ValidationError(_('One of unregistered user or registered user \
                                    should be set.'))
        if self.unregistered_user is not None and self.registered_user is not None:
            raise ValidationError(_('Either unregistered user or registered user \
                                    can be set.'))
    def __str__(self):
        return '%s' % (self.name)


class CashRegister(models.Model):
    """Cash register used to monitor finances.

    Attributes:
        - creation_date: datetime of the creation of the cash register.
            Not editable.
        - modification_date: datetime of the last modification of the cash
            register. Not editable.
        - name: string storing the name of the cash register to be easily found.

    Relationships with other models:
        - bought_items: several bought items (see Participant) associated to this
            cash register.
        - memberships: several memberships associated to this cash register.
        - treasury_operations: several treasury operations related to this cash
            register.

    Ordering by ASCending creation_date.
    """

    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)
    name = models.CharField(_('name'), max_length=50)

    class Meta:
        verbose_name = _('cash register')
        verbose_name_plural = _('cash registers')
        ordering = ['creation_date']

    def __str__(self):
        return '%s' % (self.name)


class TreasuryOperation(models.Model):
    """Treasury operation on cash registers.

    A treasury operation is available to keep track of transfer of money to or
    from a cash register which is not linked to any fee or subvention.
    A treasury operation is typically adding petty cash or taking money from the
    cash register to put it in the bank or add it as petty cash in an other cash
    register.

    Attributes:
        - amount: float representing the amount of money taken from or added to
            the cash register.
        - creation_date: datetime of the creation of the treasury operation.
            Not editable.
        - description: string storing the description of the treasury operation.
            Can be None.
        - modification_date: datetime of the last modification of the treasury
            operation. Not editable.
        - name: string storing the name of the treasury operation to be easily
            found.

    Relationships with other models:
        - cash_register: cash register on which the treasury operation was made.

    Ordering by DESCending creation_date.
    """

    amount = models.DecimalField(_('amount'), max_digits=8, decimal_places=2)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    description = models.TextField(_('description'), blank=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)
    name = models.CharField(_('name'), max_length=50)

    cash_register = models.ForeignKey(CashRegister,
                    related_name='treasury_operations', verbose_name=_('cash register'))

    class Meta:
        verbose_name = _('treasury operation')
        verbose_name_plural = _('treasury operations')
        ordering = ['-creation_date']

    def __str__(self):
        return '%s (%s)' % (self.name, str(self.creation_date))
