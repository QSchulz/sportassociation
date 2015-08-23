from django.contrib import admin
from .models import (Location, Permanence, Equipment, Lending, Position,
                    MembershipType, Membership, PublicFile, PublicImage, ProtectedFile, ProtectedImage, AdminFile)

admin.site.register(Location)
admin.site.register(Permanence)
admin.site.register(Equipment)
admin.site.register(Lending)
admin.site.register(Position)
admin.site.register(MembershipType)
admin.site.register(Membership)
admin.site.register(PublicFile)
admin.site.register(PublicImage)
