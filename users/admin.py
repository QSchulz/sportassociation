from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import ugettext as _

admin.site.unregister(User)

class CustomUserInline(admin.StackedInline):
    model = CustomUser
    can_delete = False
    exclude = ('position',)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (CustomUserInline,)
    can_delete = False
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'first_name', 'last_name', 'email')}
        ),
        (_('Status'), {
            'classes': ('wide', 'collapse',),
            'fields': ('is_active', 'is_superuser', 'is_staff',)}
        ),
        (_('Dates'), {
            'classes': ('wide', 'collapse',),
            'fields': ('last_login', 'date_joined',)}
        ),
    )
