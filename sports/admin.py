from django.contrib import admin
from .models import (Sport, Match, Session, CancelledSession)

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

@admin.register(CancelledSession)
class CancelledSessionAdmin(admin.ModelAdmin):

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')
        
admin.site.register(Session)
