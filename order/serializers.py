from rest_framework import serializers
from .models import CartItem
from product.models import Product
from django.utils.translation import gettext_lazy as _


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'is_visible']

    def validate_quantity(self, value):
        product = self.initial_data.get('product')
        product = Product.objects.get(pk=product)

        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")

        if value > product.quantity:
            raise serializers.ValidationError(f"Only {product.quantity} items available in stock.")

        return value