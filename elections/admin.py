from django.contrib import admin
from .models import (Election, VacantPosition, Candidature, Vote)

class VacantPositionInline(admin.StackedInline):
    fields = ('position', 'elected_number', 'staying_staff',)
    filter_horizontal = ('staying_staff',)
    model = VacantPosition
    extra = 0

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'start_date', 'end_date',)
    search_fields = ('title', 'description',)
    list_filter = ('is_published', 'start_date', 'end_date',)
    ordering = ('-start_date', '-end_date',)
    fields = ('title', 'slug', 'is_published', 'start_date', 'end_date',
            'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [VacantPositionInline,]

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

@admin.register(Candidature)
class CandidatureAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'vacant_position',)
    search_fields = ('speech', 'candidate',)
    ordering = ('-vacant_position',)
    fields = ('speech', 'candidate', 'vacant_position',)
    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')
