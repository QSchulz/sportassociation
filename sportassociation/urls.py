"""sportassociation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from communication.views import HomeView

from . import settings
from users.views import AdminUserCreateView

urlpatterns = [
    #Comment the next line if you don't want to create users with random passwords.
    url(r'^admin/users/customuser/add/$', AdminUserCreateView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^communication/', include('communication.urls', namespace='communication')),
    url(r'^activities/', include('activities.urls', namespace='activities')),
    url(r'^sports/', include('sports.urls', namespace='sports')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
