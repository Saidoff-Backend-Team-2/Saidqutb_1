from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework import generics
from .models import Contacts, SocialMedia, ContactWithUs
from .serializers import ContactsSerializer, SocialMediaSerializer, ContactWithUsSerializer

from .models import *
from .serializers import *
from .models import Banner


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


class ContactsView(generics.RetrieveAPIView):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer

    def get_object(self):
        return self.queryset.first()


class SocialMediaListView(generics.ListAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer


class ContactWithUsCreateView(generics.CreateAPIView):
    queryset = ContactWithUs.objects.all()
    serializer_class = ContactWithUsSerializer





