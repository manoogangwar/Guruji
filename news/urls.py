from django.urls import path
from .views import NewsListView, NewsDetailView, NewsApiView

urlpatterns = [
    path('news/', NewsListView.as_view(), name='news_list'),
    path('api/news/', NewsApiView.as_view(), name='news_api'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),

]    



