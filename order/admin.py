from django.contrib import admin
from .models import Order, CartItem, OrderStatus, OrderMinSum

admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(OrderMinSum)
