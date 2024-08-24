from django.urls import path
from .views import BannerListView, AboutUsHomeView, ContactsView, SocialMediaListView, ContactWithUsCreateView


urlpatterns = [
    path('banners', BannerListView.as_view(), name='banner-list'),
    path('about-us/home/', AboutUsHomeView.as_view(), name='about-us-home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('social-media/', SocialMediaListView.as_view(), name='social-media'),
    path('contact-with-us/', ContactWithUsCreateView.as_view(), name='contact-with-us'),
]