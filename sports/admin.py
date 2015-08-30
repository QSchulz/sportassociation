from django.contrib import admin
from .models import (Sport, Match, Session, CancelledSession)

class SessionInline(admin.StackedInline):
    model = Session
    extra = 0

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SessionInline,]

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

@admin.register(CancelledSession)
class CancelledSessionAdmin(admin.ModelAdmin):

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')
