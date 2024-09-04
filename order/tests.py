from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework.test import APITestCase
from account.models import User
from order.models import CartItem, Order, OrderMinSum
from product.models import Product


User = get_user_model()

class CartItemTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpass'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.product = Product.objects.create(title="Test Product", price=100, quantity=10)

    def test_create_cart_item(self):
        url = reverse('cartitem-create')
        data = {"product": self.product.id, "quantity": 2}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)
        cart_item = CartItem.objects.get(user=self.user, product=self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(self.product.quantity, 8)

    def test_create_cart_item_exceed_quantity(self):
        url = reverse('cartitem-create')
        data = {"product": self.product.id, "quantity": 20}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Only 10 items available in stock.", response.content.decode())

    def test_update_cart_item_quantity(self):
        cart_item = CartItem.objects.create(user=self.user, product=self.product, quantity=2)
        url = reverse('cartitem-update', args=[cart_item.id])
        data = {"quantity": 5}
        response = self.client.put(url, data, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 5)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 5)

    def test_delete_cart_item(self):
        cart_item = CartItem.objects.create(user=self.user, product=self.product, quantity=2)
        url = reverse('cartitem-delete', args=[cart_item.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 10)


class OrderTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.product = Product.objects.create(title="Test Product", price=100, quantity=10)
        self.cart_item = CartItem.objects.create(user=self.user, product=self.product, quantity=2)
        self.order_min_sum = OrderMinSum.objects.create(min_order_sum='150')

    def test_create_order(self):
        url = reverse('order-create')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 201)
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.total_price, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 8)

    def test_create_order_below_min_sum(self):
        self.cart_item.quantity = 1
        self.cart_item.save()

        url = reverse('order-create')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Total order amount must be at least 150 so'm.", response.content.decode())

    def test_cancel_order(self):
        order = Order.objects.create(user=self.user, status='created')
        CartItem.objects.filter(user=self.user).update(order=order)

        url = reverse('order-cancel', args=[order.id])
        response = self.client.put(url, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, 'cancelled')
