import requests
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models  
from .forms import *
from django.urls import reverse
from .models import *
from django.db.models import Q
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,)   
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from survey.models import UserProfile
from accounts.models import User 
from accounts.models import ContactInformation, ProfessionalInformation
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Case, When, IntegerField, Q
from django.core.paginator import Paginator
from .forms import SearchForm
from .utils import get_lat_long   


User = get_user_model()


class HomeView(View):
    def get(self, request):
        return render(request, "base/index.html")


class UserRegisterView(View):
    template_name = "accounts/registration.html"
    success_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        user_form = UserRegistrationForm()
        contact_form = ContactInformationForm()
        return render(
            request,
            self.template_name,
            {"user_form": user_form, "contact_form": contact_form},
        )

    def post(self, request, *args, **kwargs):
        user_form = UserRegistrationForm(request.POST)
        contact_form = ContactInformationForm(request.POST)

        if user_form.is_valid() and contact_form.is_valid():
            phone = contact_form.cleaned_data.get("phone")

            if User.objects.filter(phone=phone).exists():
                contact_form.add_error("phone", "This phone is already registered")
                return render(
                    request,
                    self.template_name,
                    {"user_form": user_form, "contact_form": contact_form},
                )

            user = user_form.save(commit=False)
            user.phone = phone
            user.save()

            contact = contact_form.save(commit=False)
            contact.user = user

            address = contact_form.cleaned_data.get("address")
            if address:
                lat, lon = get_lat_long(address)
                contact.latitude = lat
                contact.longitude = lon

            contact.save()

            messages.success(request, "Account created! Please login.")
            return redirect(self.success_url)

        return render(
            request,
            self.template_name,
            {"user_form": user_form, "contact_form": contact_form},
        )


class UserLoginView(LoginView):
    form_class = CustomAuthForm
    template_name = "accounts/login.html"

    def post(self, request, *args, **kwargs):
        username_or_email = request.POST.get("username")
        password = request.POST.get("password")

        # authenticate by username OR email
        user = User.objects.filter(
            models.Q(username=username_or_email) | models.Q(email=username_or_email)
        ).first()

        if user and user.check_password(password):
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")
            return render(request, self.template_name, {"form": self.form_class()})


# ---- PROFILE UPDATE ----
class UpdateProfileView(LoginRequiredMixin, View):
    success_url = reverse_lazy("profile")

    def post(self, request):
        user_form = UserRegistrationForm(request.POST, instance=request.user)
        contact_info, created = ContactInformation.objects.get_or_create(user=request.user)
        contact_form = ContactInformationForm(request.POST, instance=contact_info)

        if user_form.is_valid() and contact_form.is_valid():
            user_form.save()
            contact_form.save()
            messages.success(request, "Profile Updated Successfully!")
            return redirect(self.success_url)

        # Agar error aaye to wapas profile page hi dikhao, same forms ke sath
        context = {
            "user_form": user_form,
            "contact_form": contact_form,
        }
        return render(request, "accounts/profile.html", context)
    
    
# ------ professional_information -----

class UpdateProfessionalInfoView(LoginRequiredMixin, View):
    success_url = reverse_lazy("profile")

    def post(self, request):
        professional_info, _ = ProfessionalInformation.objects.get_or_create(
            user=request.user
        )
        print(professional_info.occupation, professional_info.education, professional_info.school, professional_info.organization)

        professional_form = ProfessionalInformationForm(
            request.POST, instance=professional_info
        )

        if professional_form.is_valid():
            professional_form.save()
            messages.success(request, "Professional information updated successfully!")
            return redirect(self.success_url)

        # error case: profile page dobara dikhao
        user_form = UserRegistrationForm(instance=request.user)
        contact_info, _ = ContactInformation.objects.get_or_create(user=request.user)
        contact_form = ContactInformationForm(instance=contact_info)

        context = {
            "user_form": user_form,
            "contact_form": contact_form,
            "professional_form": professional_form,
        }
        return render(request, "accounts/profile.html", context)


#-------- Forgot password ---------

class PasswordResetView(View):
    template_name = "accounts/forgot_password.html"

    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ForgotPasswordForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email=email).first()

            if not user:
                messages.error(request, "This email is not registered.")
                return render(request, self.template_name, {"form": form})

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_url = reverse(
                "password_reset_confirm",
                kwargs={"uidb64": uid, "token": token}
            )

            reset_link = request.build_absolute_uri(reset_url)

            send_mail(
                "Reset Your Password",
                f"Click the link to reset your password:\n{reset_link}",
                "noreply@example.com",
                [email],
            )

            messages.success(
                request,
                "Password reset link sent to your email."
            )
            return redirect("login")

        return render(request, self.template_name, {"form": form})


# ---- PROFILE PAGE ----

class UserProfileView(LoginRequiredMixin, View):
    login_url = "login"
    redirect_field_name = "next"

    def get(self, request):
        # yahan forms banake profile.html ko bhejenge
        user_form = UserRegistrationForm(instance=request.user)
        contact_info, created = ContactInformation.objects.get_or_create(user=request.user)
        contact_form = ContactInformationForm(instance=contact_info)
        professional_info, created = ProfessionalInformation.objects.get_or_create(user=request.user)
        professional_form = ProfessionalInformationForm(instance=professional_info)     
        

        context = {
            "user_form": user_form,
            "contact_form": contact_form,
            "professional_form":professional_form,
        }
        return render(request, "accounts/profile.html", context)


class UserLogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            request.session.flush()
        return redirect("login")



@method_decorator(csrf_exempt, name='dispatch')
class GetStatesView(View):
    def get(self, request, *args, **kwargs):
        country_code = request.GET.get("country")  # IN, US
        
        states = []
        if country_code:
            try:
                response = requests.post(
                    "https://countriesnow.space/api/v0.1/countries/states",
                    json={"iso2": country_code}
                )

                data = response.json()
    
                if data.get("data"):
                    states = [s["name"] for s in data["data"]["states"]]

            except requests.RequestException:
                return JsonResponse({
                    "states": [],
                    "error": "Unable to fetch states"
                })

        return JsonResponse({"states": states})


#----- Community Search ------

class SangatSearchFormView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        return render(request, "accounts/search_form.html")


class SangatSearchResultView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        filters = Q()

        country = request.GET.get("country", "").strip()
        state = request.GET.get("state", "").strip()
        city = request.GET.get("city", "").strip()
        occupation = request.GET.get("occupation", "").strip()

        if country:
            filters &= Q(contact_info__country__icontains=country)
        if state:
            filters &= Q(contact_info__state__icontains=state)
        if city:
            filters &= Q(contact_info__city__icontains=city)
        if occupation:
            filters &= Q(professional_info__occupation__icontains=occupation)

        if not filters:
            return render(
                request,
                "accounts/search_results.html",
                {
                    "users": [],
                    "error": "Please enter at least one search field"
                }
            )

        users = User.objects.select_related(
            "contact_info", "professional_info"
        ).filter(filters).distinct()

        if not users.exists():
            return render(
                request,
                "accounts/search_results.html",
                {
                    "users": [],
                    "error": "No results found"
                }
            )

        return render(request, "accounts/search_results.html",{"users": users})


class SendContactRequestView(LoginRequiredMixin, View):
    login_url = "login"

    def post(self, request, user_id):
        receiver = get_object_or_404(User, id=user_id)

        if receiver == request.user:
            messages.error(request, "You cannot send request to yourself.")
            return redirect("sangat_search_results")

        contact_request, created = ContactRequest.objects.get_or_create(
            sender=request.user,
            receiver=receiver
        )

        if created:
            messages.success(request, "Contact request sent successfully!")
        else:
            messages.warning(request, "Contact request already sent.")

        return redirect("search")


