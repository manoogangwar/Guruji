from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, ContactInformation, ProfessionalInformation, ContactRequest, MemberProfile, PrivacySettings, CommunicationPreferences
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

# Inline MemberProfile
class MemberProfileInline(admin.StackedInline):
    model = MemberProfile
    can_delete = False
    verbose_name_plural = 'Member Profiles'
    verbose_name = 'Member Profile'
    fk_name = 'user' 
    extra = 0  

    fieldsets = (
        ('Basic Information', {
            'fields': ('bio',)
        }),
        ('Profile Picture', {
            'fields': ('profile_picture',),
        }),
        ('Other Details', {
            'fields': ('last_updated',),
        }),
    )
    
    readonly_fields = ('last_updated',) 


class PrivacySettingsInline(admin.StackedInline):
    model = PrivacySettings
    can_delete = False
    verbose_name_plural = 'Privacy Settings'
    verbose_name = 'Privacy Setting'

    fieldsets = (
        ('Privacy Preferences', {
            'fields': (
                'profile_visibility', 
                'bio_visibility', 
                'profile_picture_visibility', 
                'contact_info_visibility', 
                'visible_on_map',
                'email_visibility',
                'address_visibility',
            ),
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'profile_visibility':
            formfield.label = "Public Profile Visibility"
            formfield.help_text = "Toggle whether your profile is visible to others."
        elif db_field.name == 'bio_visibility':
            formfield.label = "Bio Visibility"
            formfield.help_text = "Choose whether your bio should be visible to others."
        elif db_field.name == 'profile_picture_visibility':
            formfield.label = "Profile Picture Visibility"
            formfield.help_text = "Control whether others can see your profile picture."
        elif db_field.name == 'contact_info_visibility':
            formfield.label = "Contact Information Visibility"
            formfield.help_text = "Toggle whether your contact details are visible to others."
        elif db_field.name == 'visible_on_map':
            formfield.label = "Visible on Map"
            formfield.help_text = "Allow others to locate you on the community map."
        return formfield


class CommunicationPreferencesInline(admin.StackedInline):
    model = CommunicationPreferences
    can_delete = False
    verbose_name_plural = 'Communication Preferences'


# Contact Information Admin
@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ("user", "get_phone", "country", "city")

    def get_phone(self, obj):
        return obj.phone or obj.user.phone
    get_phone.short_description = 'Phone'

# Professional Information Admin
@admin.register(ProfessionalInformation)
class ProfessionalInformationAdmin(admin.ModelAdmin):
    list_display = ("user", "occupation", "organization")

# Contact Request Admin
@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "created_at")
