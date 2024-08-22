from django.urls import path
from .views import BannerListView, AboutUsHomeView


urlpatterns = [
    path('banners', BannerListView.as_view(), name='banner-list'),
    path('about-us/home/', AboutUsHomeView.as_view(), name='about-us-home')
]