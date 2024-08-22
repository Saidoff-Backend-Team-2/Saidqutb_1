from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import Media
from phonenumber_field.modelfields import PhoneNumberField


class Product(models.Model):
    title = models.CharField(_('title'), max_length=255)
    desc = models.TextField(_('desc'))
    size = models.CharField(_('size'), help_text='in liters')
    image = models.OneToOneField(Media, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.title}-{self.size}"

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, related_name='attributes', on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=255)
    value = models.CharField(_('title'), max_length=255)

    def __str__(self):
        return f"{self.product.title} - {self.title}: {self.value}"

    class Meta:
        verbose_name = _("Product's Attribute")
        verbose_name_plural = _("Products' Attributes")


class WebOrder(models.Model):
    full_name = models.CharField(_('full_name'), max_length=255)
    phone_number = PhoneNumberField(_('phone_number'))

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _('Orders')
