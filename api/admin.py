from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Job, Contact, Document


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "is_staff", "is_superuser", "is_active")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_superuser", "is_active"),
        }),
    )

    search_fields = ("email",)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Job)
admin.site.register(Contact)
admin.site.register(Document)