from django.shortcuts import render
from rest_framework import generics
from rest_framework.throttling import UserRateThrottle

from .models import Product, WebOrder
from .serializers import ProductHomeListSerializer, WebOrderSerializer, ProductListSerializer


class ProductHomeListView(generics.ListAPIView):
    queryset = Product.objects.all()[:10]
    serializer_class = ProductHomeListSerializer


class WebOrderCreateView(generics.CreateAPIView):
    queryset = WebOrder.objects.all()
    serializer_class = WebOrderSerializer
    throttle_classes = [UserRateThrottle, ]


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
