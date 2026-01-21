from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django_countries.fields import CountryField
from .managers import UserManager
from .country_prefix import PHONE_NUMBER_PREFIX_CHOICES_NAME


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_prefix = models.CharField(max_length=5, choices=PHONE_NUMBER_PREFIX_CHOICES_NAME, default="+91")
    phone = models.CharField(max_length=15, unique=True)

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email", "phone"]

    objects = UserManager()

    def __str__(self):
        return self.username



class ContactInformation(models.Model):

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="contact_info")
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)

    address = models.TextField(blank=True)
    country = CountryField(blank=True)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Contact Info"



class ProfessionalInformation(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="professional_info"
    )

    occupation = models.CharField(max_length=100, blank=True)
    education = models.CharField(max_length=150, blank=True)
    school = models.CharField(max_length=150, blank=True)
    organization = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.user.username} Professional Info"



class MemberProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="member")
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_picture/", blank=True, null=True)
    last_updated = models.DateField(auto_now=True)



class PrivacySettings(models.Model):
    CHOICE = [('public', 'Public'), ('private', 'Private')]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='privacy_settings')
    profile_visibility = models.BooleanField(default=True)
    bio_visibility = models.BooleanField(default=True)
    profile_picture_visibility = models.BooleanField(default=True)
    contact_info_visibility = models.BooleanField(default=True)
    email_visibility = models.BooleanField(default=True)
    address_visibility = models.BooleanField(default=False)
    visible_on_map = models.BooleanField(default=True)


class CommunicationPreferences(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='communication_preferences')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    marketing_emails = models.BooleanField(default=False)


class ContactRequest(models.Model):
    sender = models.ForeignKey(
        User,
        related_name="sent_requests",
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User,
        related_name="received_requests",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("sender", "receiver")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sender} → {self.receiver}"
