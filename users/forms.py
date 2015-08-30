from django import forms

class AdminUserForm(forms.Form):

    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    id_photo = forms.ImageField()
