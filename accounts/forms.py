from django import forms 
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or Email",
        max_length=250
    )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError("Your account is inactive.")


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name","password1","password2"]


class ContactInformationForm(forms.ModelForm):
    class Meta:
        model = ContactInformation
        fields = [
            "phone",
            "dob",
            "gender",
            "address",
            "country",
            "state",
            "city",
            "postal_code",
        ]

        widgets = {
            "dob": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "gender": forms.Select(
                choices=[
                    ("Male", "Male"),
                    ("Female", "Female"),
                    ("Other", "Other"),
                ],
                attrs={"class": "form-control"}
            ),
            "address": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "country": CountrySelectWidget(attrs={"class": "form-control"}),
            "state": forms.Select(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }

    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

class ProfessionalInformationForm(forms.ModelForm):
    class Meta:
        model = ProfessionalInformation
        fields = ["occupation", "education", "school", "organization"]

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()



class SearchForm(forms.Form):
    country = forms.CharField(required=False, max_length=100)
    state = forms.CharField(required=False, max_length=100)
    city = forms.CharField(required=False, max_length=100)
    occupation = forms.CharField(required=False, min_length=2, max_length=100)

    def clean(self):
        cleaned_data = super().clean()

        if not any(cleaned_data.values()):
            raise forms.ValidationError(
                "Please enter at least one field to search."
            )

        return cleaned_data
