from django.shortcuts import (render, get_object_or_404)
from django.http import HttpResponseRedirect
from .forms import AdminUserForm
from .models import CustomUser
from sportassociation import settings
from django.views.generic import (View, DetailView, UpdateView)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils import text
from django.core.exceptions import ObjectDoesNotExist
from smtplib import SMTPException
from django.core.urlresolvers import reverse_lazy

class AdminUserCreateView(View):
    initial = {'form': AdminUserForm()}
    template_name = 'users/create.html'

    def get(self, request):
        return render(request, self.template_name, self.initial)

    def post(self, request):
        form = AdminUserForm(request.POST, request.FILES)
        if form.is_valid():
            password = User.objects.make_random_password()
            user = User(email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'])
            user.set_password(password)
            user.username = text.slugify(user.first_name) + "." + text.slugify(user.last_name)
            user.username = user.username[:30]
            counter = 0
            try:
                while True:
                    User.objects.get(username=user.username)
                    last_letter_index = 30-len(str(counter))
                    user.username = user.username[:last_letter_index] + str(counter)
                    counter+=1
            except ObjectDoesNotExist:
                pass
            #TODO: Catch exceptions and if occuring, rollback the transactions
            #below.
            user.save()
            customUser = CustomUser(user=user, id_photo=request.FILES['id_photo'])
            customUser.save()

            #Create the email content and send it.
            content = {'username': user.username, 'first_name': user.first_name,
                        'password': password}
            mail_content_txt = render_to_string('users/mail_new.txt', content)
            mail_content_html = render_to_string('users/mail_new.html', content)
            try:
                send_mail(_('Welcome to BDS !'),
                            mail_content_txt,
                            settings.EMAIL_HOST_USER,
                            [user.email],
                            html_message=mail_content_html)
            except SMTPException:
                messages.add_message(request, messages.ERROR, _('Failed to send \
                                    credentials by mail.'))
            return HttpResponseRedirect('/admin/users/customuser/%s' % (customUser.id))
        return render(request, self.template_name, {'form': form})

    @method_decorator(permission_required('users.add_customuser'))
    def dispatch(self, *args, **kwargs):
        return super(AdminUserCreateView, self).dispatch(*args, **kwargs)


class AccountView(DetailView):
    model = CustomUser

    def get_object(self, queryset=None):
        return self.request.user.customuser

class AccountEdit(UpdateView):
    model = CustomUser
    success_url = reverse_lazy('users:account')
    fields=['nickname', 'birthdate', 'gender', 'global_scope', 'phone_scope',
        'mail_scope', 'phone', 'size']

    def get_object(self, queryset=None):
        return self.request.user.customuser

class DisplayView(DetailView):
    model = CustomUser
