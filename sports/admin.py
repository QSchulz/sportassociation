from django.contrib import admin
from .models import (Sport, Match, Session, CancelledSession)

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Match)
admin.site.register(Session)
admin.site.register(CancelledSession)
