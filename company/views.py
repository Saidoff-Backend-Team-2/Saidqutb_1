from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from .models import *
from .serializers import *
from company.models import Banner


class BannerListView(APIView):
    def get(self, request, *args, **kwargs):
        banners = Banner.objects.all()
        if not banners.exists():
            return Response({'error': "No banners found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = BannerListSerializers(banners, many=True, context={'request': request})
        return Response(data=serializer.data)


class AboutUsHomeView(APIView):
    def get(self, request, *args, **kwargs):
        about_us = AboutUs.objects.last()
        serializer = AboutUsHomeSerializer(about_us, context={'request': request})
        return Response(data=serializer.data)






