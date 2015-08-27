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

admin.site.register(Location)
admin.site.register(Permanence)
admin.site.register(Equipment)
admin.site.register(Lending)
admin.site.register(Position)
admin.site.register(MembershipType)
admin.site.register(Membership)
admin.site.register(PublicFile)
admin.site.register(PublicImage)
