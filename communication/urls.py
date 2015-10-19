from django.conf.urls import include, url
from .views import (NewsView, ArticlesView, ArticleView, WeekmailsView, WeekmailView)

urlpatterns = [
    url(r'^news', NewsView.as_view(), name='news'),
    url(r'^articles', ArticlesView.as_view(), name='articles'),
    url(r'^article/(?P<pk>[0-9]+)/(?P<slug>[-\w]+)', ArticleView.as_view(), name='article'),
    url(r'^weekmails', WeekmailsView.as_view(), name='weekmails'),
    url(r'^weekmail/(?P<pk>[0-9]+)', WeekmailView.as_view(), name='weekmail'),
]

'''
    url(r'^activities/', include('activities.urls', namespace='activities')),
    #url(r'^articles/', include('communication.urls', namespace='communication')),
    url(r'^sports/', include('sports.urls', namespace='sports')),
    #url(r'^elections/', include('elections.urls', namespace='elections')),
    #url(r'^users/', include('users.urls', namespace='users')),
'''
