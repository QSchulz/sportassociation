from django.contrib import admin
from .models import (Election, VacantPosition, Candidature, Vote)

class VacantPositionInline(admin.StackedInline):
    model = VacantPosition
    extra = 0

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [VacantPositionInline,]

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

@admin.register(Candidature)
class CandidatureAdmin(admin.ModelAdmin):

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')
