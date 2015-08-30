from django import forms
from django.contrib.auth.models import User
from .models import (GENDERS, SCOPES, SCOPE_REGISTERED, SCOPE_MANAGER,
                    SCOPE_STAFF, SCOPE_MEMBER, SHIRT_SIZES)
from django.core.validators import RegexValidator
from django.forms.extras.widgets import SelectDateWidget
from datetime import datetime

GENDERS_PLUS_EMPTY = (('', '-------'),) + GENDERS
SHIRT_SIZES_PLUS_EMPTY = (('', '-------'),) + SHIRT_SIZES

class AdminUserForm(forms.Form):

    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    id_photo = forms.ImageField()
