from django.contrib import admin
from .models import (Election, VacantPosition, Candidature, Vote)

admin.site.register(Election)
admin.site.register(VacantPosition)
admin.site.register(Candidature)
admin.site.register(Vote)
