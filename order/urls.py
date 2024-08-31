from django.urls import path
from .views import CartItemListView, CartItemCreateView, CartItemUpdateView, CartItemDeleteView

urlpatterns = [
    path('cart-items/', CartItemListView.as_view(), name='cartitem-list'),
    path('cart-items/add/', CartItemCreateView.as_view(), name='cartitem-create'),
    path('cart-items/update/<int:pk>/', CartItemUpdateView.as_view(), name='cartitem-update'),
    path('cart-items/delete/<int:pk>/', CartItemDeleteView.as_view(), name='cartitem-delete'),
]