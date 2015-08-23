from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.unregister(User)

class CustomUserInline(admin.StackedInline):
    model = CustomUser

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (CustomUserInline,)
    can_delete = False
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')}
        ),
    )
    prepopulated_fields = {'email': ('username',)}
