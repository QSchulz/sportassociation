"""Class and enumerations related to the management of users.

This exports:
    - MALE: equals to 'M'. Used in GENDER enumeration.
    - FEMALE: equals to 'F'. Used in GENDER enumeration.
    - GENDERS: enumeration for human gender.
    - SCOPE_REGISTERED: equals to 1. Used in SCOPES enumeration. The variable
        protected by this scope is limited to registered users and above.
    - SCOPE_MEMBER: equals to 2. Used in SCOPES enumeration. The variable
        protected by this scope is limited to current members and above.
    - SCOPE_MANAGER: equals to 3. Used in SCOPES enumeration. The variable
        protected by this scope is limited to users who manage sports and above.
    - SCOPE_STAFF: equals to 4. Used in SCOPES enumeration. The variable
        protected by this scope is limited to staff users.
    - SCOPES: enumeration for privacy scopes.
    - SHIRT_SIZES: enumeration for shirt sizes. Either 'S', 'M', 'L' or 'XL'.

    - CustomUser: class representing the user.
"""
from django.db import models
from sorl.thumbnail import ImageField
from django.contrib.auth.models import User
from django.core.validators import (RegexValidator, MaxValueValidator,
                                    MinValueValidator)
from django.utils.translation import ugettext as _
from datetime import date
from django.core.exceptions import (ObjectDoesNotExist, ValidationError)

MALE = 'M'
FEMALE = 'F'

GENDERS = (
    (MALE, 'Male'),
    (FEMALE, 'Female')
)

SCOPE_REGISTERED = 1
SCOPE_MEMBER = 2
SCOPE_MANAGER = 3
SCOPE_STAFF = 4

SCOPES = (
    (SCOPE_REGISTERED, _('Registered users')),
    (SCOPE_MEMBER, _('Members')),
    (SCOPE_MANAGER, _('Managers')),
    (SCOPE_STAFF, _('Staff'))
)

SHIRT_SIZES = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
)


class CustomUser(models.Model):
    """Model representing a user.

     This class have a OneToOne relation with django.contrib.auth.models.User to
     be able to use the authentication modules.
     Email address is used as username.
     To be able to add users, staff members can either be superuser or have
     permissions to add or modify user (which is similar to being a superuser).

     Privacy matters, please respect scopes (see SCOPES enumeration).

     Inherited attributes from django.contrib.auth.models.User:
        - date_joined: datetime of the creation of the user.
        - email: string storing the email of the user (used as username).
        - first_name: string storing the first name of the user.
        - is_active: boolean indicating if the user can authenticate (used for
            bans). Prefer setting to False instead of deleting a user.
        - is_staff: boolean indicating if the user has access to the admin site.
        - is_superuser: boolean indicating if the user can add or modify users.
        - last_login: datetime of the last time the user logged in.
        - last_name: string storing the last name of the user.
        - password: string storing the password of the user after encryption.
        - username: string storing the username of the user (equals to email).

    Attributes:
        - user: the one to one relationship with django.contrib.auth.models.User
        - birthdate: date of birth of the user. Can be None.
        - competition_expiration: date of expiration of the competition
            license. Can be None.
        - competition_license: string storing the competition license number of
            the user.
        - diffusion_authorisation: boolean indicating if the user gave his
            agreement on the diffusion of his/her photos.
        - gender: value of GENDERS enumeration indicating the gender of the user.
            Can be None.
        - global_scope: value of SCOPES enumeration indicating the privacy scope
            for the user profile.
        - id_photo: image of the user.
        - modification_date: datetime of the last modification of the user.
            Not editable.
        - mail_scope: value of SCOPES enumeration indicating the privacy scope
            for the email address.
        - nickname: string storing the nickname of the user. Can be None.
        - phone: string storing the phone number of the user.
            Format: +99 9 99 99 99 (up to 15 digits).
        - phone_scope: value of SCOPES enumeration indicating the privacy scope
            for the phone number.
        - size: value of SHIRT_SIZES enumeration indicating the sweat or t-shirt
            size.

    Relationships with other models:
        - authored_articles: several articles authored by this user.
        - candidatures: several candidatures from this user to different elections.
        - competition_sports: several sports in which the user is competing.
        - financial_operations: several fees or subventions paid or given by the
            user.
        - kept_positions: several positions kept through elections processes.
        - lendings: several lendings by this user.
        - managed_sessions: several sessions managed by this user.
        - managed_sports: several sports managed by this user.
        - membership_history: several memberships associated to this user.
        - participations: several participations to activities associated to this
            user.
        - subscribed_sports: several sports to which the user has subscribed to
            receive news.
        - votes: several votes associated to this user.

    Methods:
        - is_manager: return True if the user is the manager of at least one sport.
        - is_member: return True if the user is currently a member (membership
            fees paid for the ongoing semester/year).
    """

    user = models.OneToOneField(User)

    birthdate = models.DateField(null=True, blank=True)
    competition_license = models.CharField(max_length=15, blank=True)
    competition_expiration = models.DateField(null=True, blank=True)
    diffusion_authorisation = models.BooleanField(default=True)
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True)
    global_scope = models.PositiveSmallIntegerField(choices=SCOPES, default=1,
                    validators = [MaxValueValidator(SCOPE_MANAGER),
                                MinValueValidator(SCOPE_REGISTERED)])
    id_photo = ImageField(upload_to='protected/users/')
    mail_scope = models.PositiveSmallIntegerField(choices=SCOPES, default=1,
                    validators = [MinValueValidator(SCOPE_REGISTERED),])
    modification_date = models.DateTimeField(auto_now=True)
    nickname = models.CharField(max_length=20, blank=True)
    phone_regex = RegexValidator(regex = r'^\+?1?\d{9,15}$',
                    message = "Phone number must be entered in the format: \
                    '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(max_length=16, validators = [phone_regex,],
            blank=True)
    phone_scope = models.PositiveSmallIntegerField(choices=SCOPES, default=1,
                    validators = [MinValueValidator(SCOPE_REGISTERED),])
    size = models.CharField(max_length=2, choices=SHIRT_SIZES, blank=True)

    position = models.ForeignKey('management.Position', related_name='users',
                null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def is_member(self):
        last_membership = self.last_membership()
        if last_membership:
            return last_membership.expiration_date >= date.today()
        else:
            return False

    def is_manager(self):
        return self.managed_sports.exists()

    def last_membership(self):
        try:
            return self.membership_history.latest('expiration_date')
        except ObjectDoesNotExist:
            return None

    def __str__(self):
        return '%s (%s)' % (self.user.get_full_name(), self.id)
