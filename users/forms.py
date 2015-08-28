from django import forms
from django.contrib.auth.models import User
from .models import (GENDERS, SCOPES, SCOPE_REGISTERED, SCOPE_MANAGER,
                    SCOPE_STAFF, SCOPE_MEMBER, SHIRT_SIZES)
from django.core.validators import RegexValidator
from django.forms.extras.widgets import SelectDateWidget

GENDERS_PLUS_EMPTY = (('', '-------'),) + GENDERS
SHIRT_SIZES_PLUS_EMPTY = (('', '-------'),) + SHIRT_SIZES

class AdminUserForm(forms.Form):

    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    id_photo = forms.ImageField()

    birthdate = forms.DateField(widget=SelectDateWidget, required=False)
    competition_license = forms.CharField(required=False)
    competition_expiration = forms.DateField(widget=SelectDateWidget, required=False)
    gender = forms.TypedChoiceField(choices=GENDERS_PLUS_EMPTY, required=False)
    nickname = forms.CharField(max_length=20, required=False)
    phone_regex = RegexValidator(regex = r'^\+?1?\d{9,15}$',
                    message = "Phone number must be entered in the format: \
                    '+999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(max_length=16, validators = [phone_regex,],
            required=False)
    size = forms.TypedChoiceField(choices=SHIRT_SIZES_PLUS_EMPTY, required=False)
