from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django_admin_bootstrapped.admin.models import SortableInline
from .models import (Weekmail, Paragraph, Article, Information)
from management.models import PublicFile

class ParagraphSortable( SortableInline, admin.StackedInline):
    model = Paragraph
    extra = 0

class PublicFileInline(GenericTabularInline):
    model = PublicFile

@admin.register(Weekmail)
class WeekmailAdmin(admin.ModelAdmin):
    inlines = [ParagraphSortable, PublicFileInline,]

admin.site.register(Article)
admin.site.register(Information)
