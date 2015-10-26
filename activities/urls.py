from django.conf.urls import include, url
from .views import (OverviewView, DetailView, BigActivitiesView, ActivitiesView)

urlpatterns = [
    url(r'^activities/$', ActivitiesView.as_view(), name='activities'),
    url(r'^big-activities/$', BigActivitiesView.as_view(), name='big-activities'),
    url(r'^(?P<pk>[0-9]+)/(?P<slug>[-\w]+)/$', DetailView.as_view(),
        name='activity'),
    url(r'^(?P<pk>[0-9]+)/$', DetailView.as_view(), name='activity'),
    url(r'^$', OverviewView.as_view(), name='overview'),
]
