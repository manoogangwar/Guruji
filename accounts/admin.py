from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, ContactInformation, ProfessionalInformation, ContactRequest
from .forms import UserRegistrationForm  

# Custom User admin
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    model = User
    add_form = UserRegistrationForm 
    form = UserRegistrationForm   

    list_display = ("username", "email", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "is_active")
    ordering = ("username",)
    
    readonly_fields = ("last_login", "date_joined")

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

# Simple admin for related models
@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "country", "city")

@admin.register(ProfessionalInformation)
class ProfessionalInformationAdmin(admin.ModelAdmin):
    list_display = ("user", "occupation", "organization")


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "created_at")