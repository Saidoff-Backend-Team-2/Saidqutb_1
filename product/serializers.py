from rest_framework import serializers
from common.serializers import MediaURLSerializer
from .models import Product, WebOrder, ProductAttribute


class ProductHomeListSerializer(serializers.ModelSerializer):
    image = MediaURLSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'desc', 'image')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['title'] = f"{instance.title} {instance.size}"
        data['desc'] = instance.desc[:20] + " " + instance.attributes.first().title + " / " + instance.size
        return data


class WebOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebOrder
        fields = '__all__'


class ProductAttributeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ('title', 'value')


class ProductListSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeListSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'desc', 'attributes')


