import uuid
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from account.models import User
from product.models import Product


class OrderStatus(models.TextChoices):
    CREATED = 'created', _('Created')
    DELIVERED = 'delivered', _('Delivered')
    CANCELLED = 'cancelled', _('Cancelled')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    address = models.TextField(_('address'))
    long = models.FloatField(_('longitude'), blank=True, null=True)
    lat = models.FloatField(_('latitude'), blank=True, null=True)
    status = models.CharField(_('status'), max_length=20, choices=OrderStatus.choices, default=OrderStatus.CREATED)
    phone_number = PhoneNumberField(_('phone number'))
    total_price = models.FloatField(_('total price'), blank=True, null=True)
    number = models.CharField(_('order number'), max_length=10, unique=True, blank=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.full_name}"

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = str(uuid.uuid4().hex[:6])
        super().save(*args, **kwargs)
        if not self.total_price:
            total_price = self.cartitem_set.aggregate(Sum('product__price'))['product__price__sum'] or 0
            self.total_price = total_price
            super().save(update_fields=['total_price'])


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    quantity = models.IntegerField(_('quantity'))
    is_visible = models.BooleanField(_('is_visible'), default=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('order'))

    def __str__(self):
        return f"{self.product.title} ({self.quantity})"

    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')


class OrderMinSum(models.Model):
    min_order_sum = models.CharField(_('minimum order sum'), max_length=255)

    def __str__(self):
        return f"Minimum order sum: {self.min_order_sum}"

    class Meta:
        verbose_name = _('Order Minimum Sum')
        verbose_name_plural = _('Order Minimum Sums')

