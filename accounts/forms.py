from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import FileExtensionValidator
from django_countries.widgets import CountrySelectWidget
from .models import User, ContactInformation, ProfessionalInformation, MemberProfile, PrivacySettings, CommunicationPreferences
from .country_prefix import PHONE_NUMBER_PREFIX_CHOICES_NAME
from django import forms

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or Email",
        max_length=250,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError("Your account is inactive.")



class UserRegistrationForm(UserCreationForm):
    phone_prefix = forms.ChoiceField(
        choices=PHONE_NUMBER_PREFIX_CHOICES_NAME,
        required=True,
        label="Country Code",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    phone = forms.CharField(
        max_length=15,
        required=True,
        label="Phone Number",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_prefix",
            "phone",
            "password1",
            "password2",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }



class ContactInformationForm(forms.ModelForm):
    class Meta:
        model = ContactInformation
        fields = [
            "dob",
            "gender",
            "address",
            "country",
            "state",
            "city",
            "postal_code",
        ]
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "gender": forms.Select(
                choices=ContactInformation.GENDER_CHOICES,
                attrs={"class": "form-control"}
            ),
            "address": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "country": CountrySelectWidget(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control"}),
        }



class ProfessionalInformationForm(forms.ModelForm):
    class Meta:
        model = ProfessionalInformation
        fields = ["occupation", "education", "school", "organization"]
        widgets = {
            "occupation": forms.TextInput(attrs={"class": "form-control"}),
            "education": forms.TextInput(attrs={"class": "form-control"}),
            "school": forms.TextInput(attrs={"class": "form-control"}),
            "organization": forms.TextInput(attrs={"class": "form-control"}),
        }



class MemberProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
        widget=forms.FileInput(attrs={"class": "form-control", "accept": ".jpg,.jpeg,.png"})
    )

    class Meta:
        model = MemberProfile
        fields = ["bio", "profile_picture"]
        widgets = {
            "bio": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Bio", "style": "height: 10rem;"}
            ),
        }

class PrivacySettingsForm(forms.ModelForm):
    class Meta:
        model = PrivacySettings
        fields = [
            'bio_visibility', 
            'contact_info_visibility',
            'email_visibility', 
            'address_visibility',  
            'profile_visibility',
            'profile_picture_visibility', 
            'visible_on_map',
        ]

class CommunicationPreferencesForm(forms.ModelForm):
    class Meta:
        model = CommunicationPreferences
        fields = ['email_notifications', 'sms_notifications', 'marketing_emails']



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }



class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        required=True
    )



class SearchForm(forms.Form):
    q = forms.CharField(label="search",required=False)
    l = forms.CharField(label="location",required=False)
    g = forms.ChoiceField(label='gender',required=False)
    p = forms.CharField(label="profession",required=False,widget=forms.TextInput(attrs={'placeholder': 'Profession'}))
