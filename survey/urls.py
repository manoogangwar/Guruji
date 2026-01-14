from django.urls import path
from .views import DashboardView, SurveyFormView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('survey/', SurveyFormView.as_view(), name='survey_form'),
]
