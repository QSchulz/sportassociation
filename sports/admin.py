from django.contrib import admin
from .models import (Sport, Match, Session, CancelledSession)
from management.admin import ProtectedImageInline

class SessionInline(admin.StackedInline):
    fields = ('date', 'weekday', 'start_time', 'end_time', 'location', 'manager',)
    model = Session
    extra = 0

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_open', 'mailing_list', 'creation_date',
            'modification_date',)
    search_fields = ('name', 'description', 'mailing_list',)
    list_filter = ('is_open', 'creation_date', 'modification_date',)
    ordering = ('-is_open', 'name',)
    fields = ('name', 'slug', 'mailing_list', 'is_open', 'description',
            'managers', 'competitors',)
    filter_horizontal = ('managers', 'competitors',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SessionInline,]

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'opponent', 'sport', 'result', )
    search_fields = ('name', 'opponent', 'description', 'result', )
    list_filter = ('date', 'sport',)
    date_hierarchy = 'date'
    ordering = ('-date',)
    fields = ('name', 'opponent', 'date', 'sport', 'location', 'description',
            'result', 'report',)
    inlines = [ProtectedImageInline,]

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

@admin.register(CancelledSession)
class CancelledSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'cancellation_date', 'cancelled_session', )
    search_fields = ('title', 'description', )
    list_filter = ('cancellation_date',)
    ordering = ('-cancellation_date',)
    fields = ('title', 'cancelled_session', 'cancellation_date', 'description',)

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')
