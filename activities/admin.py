from django.contrib import admin
#from sorl.thumbnail.admin import AdminImageMixin
from .models import (Activity, Parameter, Item, Participant)
from management.admin import (AdminFileInline, ProtectedFileInline,
                                ProtectedImageInline)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date', 'start_date', 'end_date',
            'is_big_activity', 'is_frontpage', 'is_member_only', 'summary',
            'creation_date', 'modification_date',)
    search_fields = ('title', 'summary')
    list_filter = ('publication_date', 'creation_date', 'modification_date',
            'start_date', 'end_date', 'is_big_activity', 'is_frontpage',
            'is_member_only',)
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    fields = ('title', 'slug', 'summary', 'website', 'cover', 'location',
            'is_big_activity', 'is_frontpage', 'is_member_only', 'start_date',
            'end_date', 'publication_date', 'content')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [AdminFileInline, ProtectedFileInline, ProtectedImageInline,]

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

class ParameterInline(admin.StackedInline):
    model = Parameter
    extra = 0

class ItemInline(admin.StackedInline):
    model = Item
    extra = 0

#@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    inlines = [ParameterInline, ItemInline]
    exclude = ('parent_parameter',)

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

#admin.site.register(Participant)
