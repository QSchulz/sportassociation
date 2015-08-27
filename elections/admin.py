from django.contrib import admin
from .models import (Election, VacantPosition, Candidature, Vote)

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(VacantPosition)
admin.site.register(Candidature)
admin.site.register(Vote)
