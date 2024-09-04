from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from account.models import User

class UserRegisterViewTest(APITestCase):

    def test_user_can_register(self):
        url = reverse('register')
        data = {
            "user_type": "individual",
            "full_name": "Test User",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "confirm_password": "testpassword123",
            "phone_number": "+998979934078",
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_passwords_must_match(self):
        url = reverse('register')
        data = {
            "user_type": "individual",
            "full_name": "Test User",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "confirm_password": "differentpassword",
            "phone_number": "+998979934078",
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username="testuser").exists())


class UserLoginViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )

    def test_user_can_login(self):
        url = reverse('login')
        data = {
            "username": "testuser",
            "password": "testpassword123"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class LogoutViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )
        self.client.force_authenticate(user=self.user)

    def test_user_can_logout(self):
        url = reverse('logout')
        tokens = self.user.get_token()
        data = {
            "refresh": tokens['refresh']
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)


class UserAccountUpdateViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )
        self.client.force_authenticate(user=self.user)

    def test_user_can_update_account(self):
        url = reverse('account')
        data = {
            "full_name": "Updated Test User",
            "email": "updatedemail@example.com"
        }

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.full_name, "Updated Test User")
        self.assertEqual(self.user.email, "updatedemail@example.com")


