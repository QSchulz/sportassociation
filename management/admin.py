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
    model = Membership
    extra = 0

@admin.register(MembershipType)
class MembershipTypeAdmin(admin.ModelAdmin):

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

admin.site.register(Location)
admin.site.register(Permanence)
admin.site.register(Equipment)
admin.site.register(Lending)
admin.site.register(PublicFile)
admin.site.register(PublicImage)
admin.site.register(ProtectedFile)
admin.site.register(ProtectedImage)
admin.site.register(AdminFile)
admin.site.register(AdminImage)
