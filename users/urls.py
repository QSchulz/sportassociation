from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from users.views import (DisplayView, AccountView, AccountEdit)

urlpatterns = [
    url(r'^account$', login_required(AccountView.as_view()), name="account"),
    url(r'^account/edit$', login_required(AccountEdit.as_view()), name="account_edit"),
    url(r'^(?P<pk>[0-9]+)$', login_required(DisplayView.as_view()), name='display'),
]
