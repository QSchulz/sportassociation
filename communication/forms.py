from django import forms
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    name = forms.CharField(label='Nom')
    mail = forms.EmailField()
    subject = forms.CharField(max_length=78, label='Objet')
    send_back = forms.BooleanField(required=False, label='Recevoir une copie')
    content = forms.CharField(widget=forms.Textarea, label='Contenu')
    captcha = CaptchaField()
