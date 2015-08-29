from django.contrib import admin
from .models import (Election, VacantPosition, Candidature, Vote)

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

@admin.register(Candidature)
class CandidatureAdmin(admin.ModelAdmin):

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

admin.site.register(VacantPosition)
admin.site.register(Vote)
