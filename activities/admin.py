from django.contrib import admin
#from sorl.thumbnail.admin import AdminImageMixin
from .models import (Activity, Parameter, Item, Participant)
from management.admin import (AdminFileInline, ProtectedFileInline,
                                ProtectedImageInline)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
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
