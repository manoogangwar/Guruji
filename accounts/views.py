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
from django.views import View
from .forms import SearchForm
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
from .utils import get_lat_long  
from django.http import JsonResponse 
from django.contrib.auth.forms import PasswordChangeForm


User = get_user_model()


class HomeView(View):
    def get(self, request):
        return render(request, "base/index.html")



class UserRegisterView(View):
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        context = {
            "user_form": UserRegistrationForm(),
            "contact_form": ContactInformationForm(),
            "professional_form": ProfessionalInformationForm(),
            "profile_form": MemberProfileForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = UserRegistrationForm(request.POST)
        contact_form = ContactInformationForm(request.POST)
        professional_form = ProfessionalInformationForm(request.POST)
        profile_form = MemberProfileForm(request.POST, request.FILES)

        if all([user_form.is_valid(), contact_form.is_valid(), professional_form.is_valid(), profile_form.is_valid()]):

            # Phone & Phone Prefix
            phone = user_form.cleaned_data.get("phone")
            phone_prefix = user_form.cleaned_data.get("phone_prefix")

            if User.objects.filter(phone=phone).exists():
                user_form.add_error("phone", "This phone is already registered")
            else:
                # Save user
                user = user_form.save(commit=False)
                user.phone = phone
                user.phone_prefix = phone_prefix
                user.save()

                # Save Contact Info
                contact = contact_form.save(commit=False)
                contact.user = user
                contact.save()

                # Save Professional Info
                professional = professional_form.save(commit=False)
                professional.user = user
                professional.save()

                # Save Profile
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                messages.success(request, "Account created! Please login.")
                return redirect(self.success_url)

        # Render back with errors
        context = {
            "user_form": user_form,
            "contact_form": contact_form,
            "professional_form": professional_form,
            "profile_form": profile_form,
        }
        return render(request, self.template_name, context)


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

class ContactUsView(View):
    template_name = "base/contact.html"
    
    def get(self, request): 
        return render(request, self.template_name)
        
    # def post(self, request):
    #     name = request.POST.get("name")
    #     email = request.POST.get("email")
    #     message = request.POST.get("message")
        
    #     ContactUs.objects.create(name=name, email=email, message=message)
    #     messages.success(request, "Message sent successfully!")
    #     return redirect("contact_us")
        
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
        uname_change = UsernameChangeForm(user=request.user)
        p_change_form = PasswordChangeForm(user=request.user)
        email_change_form = EmailChangeForm(user=request.user)

        contact_info, created = ContactInformation.objects.get_or_create(user=request.user)
        contact_form = ContactInformationForm(instance=contact_info)

        professional_info, created = ProfessionalInformation.objects.get_or_create(user=request.user)
        professional_form = ProfessionalInformationForm(instance=professional_info) 

        member_profile, _ = MemberProfile.objects.get_or_create(user=request.user)
        member_profile_form = MemberProfileForm(instance=member_profile)

        privacy_instance,created = PrivacySettings.objects.get_or_create(user=request.user)
        privacy_form = PrivacySettingsForm(instance=privacy_instance)

        comm_instance,created = CommunicationPreferences.objects.get_or_create(user=request.user)
        comm_form = CommunicationPreferencesForm(instance=comm_instance)



        context = {
            "user_form": user_form,
            "c_info": contact_form,
            "professional_form":professional_form,
            "member_profile_form": member_profile_form,
            "privacy_form":privacy_form,
            "comm_form":comm_form,
            'uname_change' : uname_change,
            'password_change_form':p_change_form,
            'email_change_form':email_change_form 
        }
        return render(request, "accounts/profile.html", context)



class UserLogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            request.session.flush()
        return redirect("login")


class PublicProfileView(LoginRequiredMixin,View):
    def get(self,request,username=None):
        user = get_object_or_404(
            User.objects.prefetch_related(
                'member', 
                'contact_info',  
                'professional_info',
                ), 
                username=username
        )
        # similar_user = get_similar_users(user)
        similar_user = None
        
        return render(request,'accounts/public_profile_view.html',{'usr':user,'smilar_usr':similar_user})



class MemberProfileHandler(LoginRequiredMixin,View):
    def post(self,request):
        instance, created = MemberProfile.objects.get_or_create(user=request.user)
        form = MemberProfileForm(request.POST,request.FILES, instance=instance)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        print('there is a error in form')
        return JsonResponse(
            {
                'success': False, 
                'error': form.errors.as_json()
                }) 

class PrivaycHandler(LoginRequiredMixin, View):
    def post(self,request):
        instance, created = PrivacySettings.objects.get_or_create(user=request.user)
        form = PrivacySettingsForm(request.POST,instance=instance)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        
        return JsonResponse(
            {
                'success': False, 
                'error': form.errors.as_json()
                }) 


class CommunicationHandler(LoginRequiredMixin,View):
    def post(self,request):
        instance, created = CommunicationPreferences.objects.get_or_create(user=request.user)
        form = CommunicationPreferencesForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        print('there is a error in form')
        return JsonResponse(
            {
                'success': False, 
                'error': form.errors.as_json()
                })   

class PasswordChangeHandler(LoginRequiredMixin,View):
    def post(self,request):
        form = PasswordChangeForm(user=request.user,data=request.POST)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        print('there is a error in form',form.errors)
        return JsonResponse(
            {
                'success': False, 
                'error': form.errors.as_json()
                }) 

class UsernameChangeHandler(LoginRequiredMixin,View):
    def post(self,request):
        form = UsernameChangeForm(user=request.user,data=request.POST)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse(
            {
                'success': False, 
                'error': form.errors.as_json()
                }) 

class EmailChangeHandler(LoginRequiredMixin,View):
    def post(self,request):
        form = EmailChangeForm(user=request.user,data=request.POST)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        print('there is a error in form',form.errors)
        return JsonResponse(
            {
                'success': False, 
                'error': form.errors.as_json()
                }) 



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

class SearchView(View):
    template_name = "accounts/search.html"
    paginate_by = 20

    def get(self, request):
        form = SearchForm(request.GET or None)
        users = User.objects.none()

        if form.is_valid():
            query = form.cleaned_data.get("q")
            location = form.cleaned_data.get("l")
            profession = form.cleaned_data.get("p")
            gender = form.cleaned_data.get("g")

            filters = Q()
            has_filter = False  

            if query:
                has_filter = True
                filters &= (
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query) |
                    Q(username__icontains=query) |
                    Q(spritual_name__icontains=query)
                )

            if profession:
                has_filter = True
                filters &= Q(
                    professional_info__occupation_detail__icontains=profession
                )

            if location:
                has_filter = True
                filters &= (
                    Q(contact_info__city__icontains=location) |
                    Q(contact_info__state__icontains=location) |
                    Q(contact_info__country__icontains=location)
                )

            if has_filter:
                users = (
                    User.objects
                    .filter(filters)
                    .select_related("professional_info", "contact_info")
                    .order_by("id")
                    .distinct()
                )

                if gender:
                    users = users.filter(gender=gender)

                paginator = Paginator(users, self.paginate_by)
                page_number = request.GET.get("page")
                users = paginator.get_page(page_number)

        return render(request, self.template_name, {
            "users": users,
            "form": form
        })



def user_search(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return JsonResponse([], safe=False)

    users = (
        User.objects
        .filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query)
        )
        .select_related('professional_info')
        [:10]
    )

    results = []

    for user in users:
        profession = (
            user.professional_info.occupation
            if hasattr(user, 'professional_info')
            else ''
        )

        results.append({
            'id': user.username,
            'name': f"{user.first_name} {user.last_name}".strip(),
            'profession': profession
        })

    return JsonResponse(results, safe=False)


def profile_completion(request):
    if request.user.is_authenticated:
        return JsonResponse({"completion": 60})
    return JsonResponse({"completion": 0})



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


