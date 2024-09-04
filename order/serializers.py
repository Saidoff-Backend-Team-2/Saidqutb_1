from calendar import month
from rest_framework import serializers
from .models import CartItem, Order
from product.models import Product
from django.utils.translation import gettext_lazy as _


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'is_visible']

    def validate(self, attrs):
        if 'product' in attrs:
            product = attrs['product']
        else:
            product = self.instance.product

        if attrs.get('quantity', 0) < 1:
            raise serializers.ValidationError({"quantity": "Quantity must be at least 1."})

        if attrs.get('quantity', 0) > product.quantity:
            raise serializers.ValidationError({"quantity": f"Only {product.quantity} items available in stock."})

        return attrs


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'long', 'lat', 'status', 'phone_number', 'total_price', 'number']
        read_only_fields = ['user', 'total_price', 'number']

