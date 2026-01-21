from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import FileExtensionValidator
from django_countries.widgets import CountrySelectWidget
from .models import *
from .country_prefix import PHONE_NUMBER_PREFIX_CHOICES_NAME
from django import forms
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError


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


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]



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

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

class MemberProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required = False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    class Meta:
        model = MemberProfile
        fields = [
            'bio','profile_picture'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio','style': 'height: 10rem;'}),
            'profile_picture': forms.FileInput(attrs={'accept':'.jpg'}),
            
        }

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['profile_picture']


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


class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'New Email'}),
        }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self,*args, **kwargs):
        email = self.cleaned_data.get('email')
        return User.objects.filter(pk=self.user.id).update(email=email)


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.user.pk).filter(email=email).exists():
            raise forms.ValidationError("This email is already taken.")
        return email

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'New Username'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self,*args, **kwargs):
        username = self.cleaned_data.get('username')
        return User.objects.filter(pk=self.user.id).update(username=username)


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(pk=self.user.pk).filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'placeholder': 'Enter your registered email'}))
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    phone_number = forms.CharField(label="Phone Number", widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        phone_number = cleaned_data.get('phone_number')

        if not User.objects.filter(email=email, username=username, phone_number=phone_number).exists():
            raise forms.ValidationError("No account matches the provided details.")
        return cleaned_data


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



class SearchForm(forms.Form):
    q = forms.CharField(label="search",required=False)
    l = forms.CharField(label="location",required=False)
    g = forms.ChoiceField(label='gender',required=False)
    p = forms.CharField(label="profession",required=False,widget=forms.TextInput(attrs={'placeholder': 'Profession'}))
