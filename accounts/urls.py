from django.urls import path
from .views import *


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("search/", SangatSearchFormView.as_view(), name="search"),
    path('search/results/', SangatSearchResultView.as_view(), name='sangat-search-results'),
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/",PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset-complete/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),  

    path("profile/personal-info/", UpdateProfileView.as_view(), name="personal-info"),
    path("profile/professional-info/", UpdateProfessionalInfoView.as_view(), name="professional-info"),

    path('member_profile_handler',MemberProfileHandler.as_view(),name='member_profile_handler'),

    path("ajax/states/", GetStatesView.as_view(), name="get_states"),
    path("contact-request/<int:user_id>/", SendContactRequestView.as_view(), name="send_contact_request"),


]
