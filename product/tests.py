from django.test import TestCase, Client
from .models import Product, WebOrder, ProductAttribute, Action
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Action
from common.models import Media
from account.models import User


class ProductHomeListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')
        self.media = Media.objects.create(file="path/to/image.jpg")
        self.discount = Discount.objects.create(title="Discount 10%", desc="Test Discount", image=self.media, percentage=10)
        self.product = Product.objects.create(
            title="Test Product",
            desc="Test Description",
            size="1L",
            image=self.media,
            price=10.99,
            discount=self.discount
        )

        ProductAttribute.objects.create(product=self.product, title="Color", value="Red")

    def test_product_home_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Test Product 1L")


class WebOrderCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('web-order')

    def test_create_web_order(self):
        data = {
            'full_name': 'John Doe',
            'phone_number': '+998979944078'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WebOrder.objects.count(), 1)
        self.assertEqual(WebOrder.objects.first().full_name, 'John Doe')


class ProductListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('product-list')
        self.media = Media.objects.create(file="path/to/image.jpg")
        self.discount = Action.objects.create(title="Discount 20%", desc="Test Discount", image=self.media, percentage=20)
        self.product = Product.objects.create(
            title="Test Product",
            desc="Test Description",
            size="1L",
            image=self.media,
            price=20.99,
            discount=self.discount
        )

        ProductAttribute.objects.create(product=self.product, title="Weight", value="1kg")

    def test_product_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Test Product")
        self.assertEqual(response.data[0]['attributes'][0]['title'], "Weight")


class DiscountDetailApiViewTest(APITestCase):

    def setUp(self):
        self.media = Media.objects.create(file='test_image.jpg')

        self.action = Action.objects.create(
            title="Test Discount",
            desc="Test Description",
            image=self.media,
            percentage=10
        )

    def test_discount_detail_view(self):
        url = reverse('discount-detail', args=[self.action.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['id'], self.action.id)
        self.assertEqual(response.data['title'], "Test Discount")
        self.assertEqual(response.data['desc'], "Test Description")
        self.assertEqual(response.data['percentage'], 10)
