from django.urls import path
from .views import UserRegisterView, UserLoginView, LogoutView, UserAccountUpdateView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/', UserAccountUpdateView.as_view(), name='account'),
]