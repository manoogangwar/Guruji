from django.urls import path
from .views import AdsListView, AdsDetailView, AdsApiView

urlpatterns = [
    path('ads/', AdsListView.as_view(), name='ads_list'),
    path('api/ads/', AdsApiView.as_view(), name='ads_api'),
    path('ads/<slug:slug>/', AdsDetailView.as_view(), name='ads_detail'),
]
