from django.contrib import admin
from django_admin_bootstrapped.admin.models import SortableInline
from .models import (Weekmail, Paragraph, Article, Information)
from management.admin import PublicFileInline
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.http import HttpResponse
import html.parser

class ParagraphSortable( SortableInline, admin.StackedInline):
    fields = ('title', 'index', 'content',)
    model = Paragraph
    extra = 0

@admin.register(Weekmail)
class WeekmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sent_date', 'creation_date', 'modification_date',)
    search_fields = ('subject', 'introduction',)
    list_filter = ('sent_date', 'creation_date', 'modification_date',)
    date_hierarchy = 'sent_date'
    ordering = ('-sent_date',)
    fields = ('subject', 'introduction', 'conclusion',)
    inlines = [ParagraphSortable, PublicFileInline,]
    actions = ['send','display',]

    def send(self, request, queryset):
        failed_weekmails = []
        for weekmail in queryset:
            if not weekmail.send():
                failed_weekmails.append(weekmail.subject)
        if failed_weekmails:
            message = _('Failed to send weekmails titled: "%s"') % \
                ('", "'.join(failed_weekmails))
        else:
            message = _('All selected weekmails have been sent.')
        self.message_user(request, message)

    def display(self, request, queryset):
        response = HttpResponse()
        html_parser = html.parser.HTMLParser()
        for weekmail in queryset:
            response.write(render_to_string('communication/display_weekmail.html',
                {'weekmail': html_parser.unescape(weekmail)}))
        return response

    send.short_description = _("Send selected weekmails")
    display.short_description = _("Display selected weekmails")

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date', 'is_frontpage', 'summary',
            'creation_date', 'modification_date',)
    search_fields = ('title', 'summary')
    list_filter = ('publication_date', 'creation_date', 'modification_date',)
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date',)
    fields = ('title', 'slug', 'summary', 'cover', 'author', 'is_frontpage',
            'publication_date', 'content')
    prepopulated_fields = {'slug': ('title',)}

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_published',
            'is_important', 'content')
    search_fields = ('title', 'content')
    list_filter = ('start_date', 'end_date', 'is_published', 'is_important',)
    date_hierarchy = 'start_date'
    ordering = ('-start_date', '-end_date')
    fields = ('title', 'start_date', 'end_date', 'is_published',
                'is_important', 'content')

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')
