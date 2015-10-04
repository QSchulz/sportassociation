from django.shortcuts import render
from django.views.generic import View
from activities.models import Activity
from sports.models import Sport
from datetime import datetime
from django.http import (HttpResponseRedirect, HttpResponse)

class HomeView(View):
    template_name = 'communication/home.html'

    def get(self, request):
        content = {}
        return render(request, self.template_name, content)

    def post(self, request):
        return HttpResponseRedirect('home')
