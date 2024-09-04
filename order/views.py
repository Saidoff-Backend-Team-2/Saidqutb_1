from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from .models import CartItem, Order, OrderMinSum
from .serializers import CartItemSerializer, OrderSerializer
from rest_framework import generics, status
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _


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
                raise serializers.ValidationError(f"Only {product.quantity} items available in stock.")
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


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        min_order_sum_obj = OrderMinSum.objects.first()
        min_order_sum = float(min_order_sum_obj.min_order_sum) if min_order_sum_obj else 0
        cart_total = CartItem.objects.filter(user=self.request.user, order__isnull=True).aggregate(
            total=Sum('product__price')
        )['total'] or 0

        if cart_total < min_order_sum:
            raise ValidationError(
                _(f"Total order amount must be at least {min_order_sum} so'm.")
            )

        order = serializer.save(user=self.request.user)
        cart_items = CartItem.objects.filter(user=self.request.user, order__isnull=True)
        cart_items.update(order=order)

        order.total_price = cart_items.aggregate(
            total=Sum('product__price')
        )['total'] or 0

        order.save()


class OrderCancelView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        order = self.get_object()
        if order.status != 'cancelled':
            order.status = 'cancelled'
            order.save()
            return Response({"status": "cancelled"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Order is already cancelled."}, status=status.HTTP_400_BAD_REQUEST)

