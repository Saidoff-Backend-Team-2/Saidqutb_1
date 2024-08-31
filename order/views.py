from itertools import product
from product.models import Product
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .models import CartItem
from .serializers import CartItemSerializer
from rest_framework import generics


class CartItemListView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user, is_visible=True, order__isnull=True)


class CartItemCreateView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        if quantity > product.quantity:
            raise serializer.ValidationError(f"Only {product.quantity} items available in stock.")

        product.quantity -= quantity
        product.save()
        serializer.save(user=self.request.user)


class CartItemUpdateView(generics.UpdateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user, is_visible=True)

    def perform_update(self, serializer):
        cart_item = self.get_object()
        new_quantity = serializer.validated_data.get('quantity', cart_item.quantity)
        product = cart_item.product

        if new_quantity > cart_item.quantity:
            delta = new_quantity - cart_item.quantity
            if delta > product.quantity:
                raise serializer.ValidationError(f"Only {product.quantity} items available in stock.")
            product.quantity -= delta
        elif new_quantity < cart_item.quantity:
            delta = cart_item.quantity - new_quantity
            product.quantity += delta

        product.save()
        serializer.save()


class CartItemDeleteView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user, is_visible=True)

    def perform_destroy(self, instance):
        product = instance.product
        product.quantity += instance.quantity
        product.save()
        instance.delete()


