from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.status import HTTP_200_OK

from .models import Banner, AboutUs, Contacts, SocialMedia, ContactWithUs
from common.models import Media

class BannerListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('banner-list')  # Замените на актуальное имя URL
        self.media = Media.objects.create(file='path/to/file.jpg', type='image')
        self.banner = Banner.objects.create(title='Test Banner', subtitle='Test Subtitle', bg_image=self.media)

    def test_get_banners(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['title'], 'Test Banner')

    def test_get_banners_empty(self):
        Banner.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())


class AboutUsHomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('about-us-home')
        self.media = Media.objects.create(file='path/to/file.jpn', type='image')
        self.about_us = AboutUs.objects.create(desc='Test Description', video=self.media)

    def test_get_about_us(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['desc'], "Test Description")


class ContactsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('contacts')
        self.contacts = Contacts.objects.create(
            address = 'Test Address',
            phone_number1='+998979934078',
            phone_number2='+998981234527',
            work_time='9.00-18.00'
        )

    def test_get_contacts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['address'], 'Test Address')


class SocialMediaListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('social-media')
        self.social_media = SocialMedia.objects.create(link='http://example.com', icon='icon_cod')

    def test_get_social_media(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['link'], 'http://example.com')


class ContactWithUsCreateViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('contact-with-us')

    def test_create_contact_with_us(self):
        data = {
            'full_name': 'Test User',
            'phone_number': '+998979934078',
            'subject': 'Test Subject',
            'message': 'Test Message'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactWithUs.objects.count(), 1)
        self.assertEqual(ContactWithUs.objects.first().full_name, 'Test User')

