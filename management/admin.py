from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import (Location, Permanence, Equipment, Lending, Position,
                    MembershipType, Membership, PublicFile, PublicImage,
                    ProtectedFile, ProtectedImage, AdminFile, AdminImage)

class AdminFileInline(GenericTabularInline):
    model = AdminFile

class AdminImageInline(GenericTabularInline):
    model = AdminImage

class ProtectedFileInline(GenericTabularInline):
    model = ProtectedFile

class ProtectedImageInline(GenericTabularInline):
    model = ProtectedImage

class PublicFileInline(GenericTabularInline):
    model = PublicFile

class PublicImageInline(GenericTabularInline):
    model = PublicImage

class MembershipInline(admin.StackedInline):
    fields = ('membership_copy', 'expiration_date', 'membership_type',
            'payment_mean', 'cheque_bank', 'cash_register', 'certificate',
            'certificate_date',)
    model = Membership
    extra = 0

@admin.register(MembershipType)
class MembershipTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'semester_fee', 'year_fee',
            'is_active',)
    search_fields = ('title', 'description',)
    list_filter = ('is_active',)
    ordering = ('-is_active', 'title',)
    fields = ('title', 'is_active', 'description', 'semester_fee', 'year_fee',)

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    search_fields = ('title', 'description',)
    ordering = ('title',)
    fields = ('title', 'description',)

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'latitude', 'longitude',)
    search_fields = ('name', 'address', 'city',)
    ordering = ('name',)
    fields = ('name', 'address', 'city', 'latitude', 'longitude',)

@admin.register(Permanence)
class PermanenceAdmin(admin.ModelAdmin):
    list_display = ('location', 'date', 'weekday', 'start_time', 'end_time',)
    list_filter = ('date', 'weekday',)
    ordering = ('-date', 'weekday',)
    fields = ('date', 'weekday', 'start_time', 'end_time', 'location',
            'related_activities',)
    filter_horizontal = ('related_activities',)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'quantity',)
    search_fields = ('name', 'description',)
    ordering = ('name',)
    fields = ('name', 'description', 'quantity',)

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

@admin.register(Lending)
class LendingAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'borrower', 'quantity', 'deposit', 'start_date',
            'end_date', 'returned',)
    list_filter = ('equipment', 'start_date', 'end_date', 'returned',)
    ordering = ('-start_date',)
    fields = ('equipment', 'borrower', 'quantity', 'deposit', 'start_date',
            'end_date', 'returned',)

admin.site.register(PublicFile)
admin.site.register(PublicImage)
admin.site.register(ProtectedFile)
admin.site.register(ProtectedImage)
admin.site.register(AdminFile)
admin.site.register(AdminImage)
