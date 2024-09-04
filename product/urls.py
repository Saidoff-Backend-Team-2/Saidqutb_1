from django.urls import path
from .views import ProductHomeListView, WebOrderCreateView, ProductListView, DiscountDetailApiView

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('home/', ProductHomeListView.as_view(), name='home'),
    path('web-order/', WebOrderCreateView.as_view(), name='web-order'),
    path('discount/<int:pk>/', DiscountDetailApiView.as_view(), name='discount-detail'),
]