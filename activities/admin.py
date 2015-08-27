from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from .models import (Activity, Parameter, Item, Participant)
from django.contrib.contenttypes.admin import GenericTabularInline
from management.models import (AdminFile, ProtectedFile, ProtectedImage)

class AdminFileInline(GenericTabularInline):
    model = AdminFile

class ProtectedFileInline(GenericTabularInline):
    model = ProtectedFile

class ProtectedImageInline(GenericTabularInline):
    model = ProtectedImage

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ AdminFileInline, ProtectedFileInline, ProtectedImageInline, ]

class ParameterInline(admin.StackedInline):
    model = Parameter
    extra = 0

class ItemInline(admin.StackedInline):
    model = Item
    extra = 0

@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    inlines = [ParameterInline, ItemInline]
    exclude = ('parent_parameter',)

admin.site.register(Participant)
