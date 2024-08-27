from django.contrib import admin
from .models import Product, ProductAttribute, WebOrder, Action


class ProductAttributeInline(admin.StackedInline):
    model = ProductAttribute
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductAttributeInline]
    list_display = ('title', 'desc', 'size')


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    pass


@admin.register(WebOrder)
class WebOrderAdmin(admin.ModelAdmin):
    pass

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    pass
