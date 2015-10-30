from django import forms
from django.utils.translation import ugettext as _

class AdminUserForm(forms.Form):

    email = forms.EmailField(label=_('Email'))
    first_name = forms.CharField(label=_('First name'))
    last_name = forms.CharField(label=_('Last name'))
    id_photo = forms.ImageField(label=_('Identity photo'))
