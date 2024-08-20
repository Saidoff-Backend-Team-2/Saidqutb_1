from django.contrib import admin
from .models import Product, ProductAttribute, WebOrder

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    pass


@admin.register(WebOrder)
class WebOrderAdmin(admin.ModelAdmin):
    pass

