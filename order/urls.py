from django.urls import path
from .views import CartItemListView, CartItemCreateView, CartItemUpdateView, CartItemDeleteView, OrderCreateView, \
    OrderCancelView

urlpatterns = [
    path('cart-items/', CartItemListView.as_view(), name='cartitem-list'),
    path('cart-items/add/', CartItemCreateView.as_view(), name='cartitem-create'),
    path('cart-items/<int:pk>/', CartItemUpdateView.as_view(), name='cartitem-update'),
    path('cart-items/<int:pk>/', CartItemDeleteView.as_view(), name='cartitem-delete'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/cancel/<int:pk>/', OrderCancelView.as_view(), name='order-cancel'),
]