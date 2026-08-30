from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Match, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("id", "email", "full_name", "tenant_name", "is_active")
    ordering = ("email",)
    search_fields = ("email", "full_name")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name", "tenant_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "full_name", "password1", "password2"),
            },
        ),
    )


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("id", "boy_name", "girl_name", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("boy_name", "girl_name", "user__email")
