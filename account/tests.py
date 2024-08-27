from .models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class UserRegisterTests(APITestCase):

    def test_register_user_success(self):
        url = reverse('register')
        data = {
            "user_type": "individual",
            "full_name": "Test User",
            "username": "testuser",
            "email": "testuser@example.com",
            "phone_number": "+1234567890",
            "password": "TestPassword123"
        }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['detail'], "Registration successful!")

    def test_register_user_existing_email(self):
        User.objects.create_user(
            username="existinguser",
            email="testuser@example.com",
            password="TestPassword123"
        )
        url = reverse('register')
        data = {
            "user_type": "individual",
            "full_name": "Test User",
            "username": "testuser2",
            "email": "testuser@example.com",
            "phone_number": "+998979934078",
            "password": "Test123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], "User with this email already exists.")

    def test_register_user_legal_without_company_name(self):
        url = reverse('register')
        data = {
            "user_type": "legal",
            "full_name": "Legal User",
            "username": "legaluser",
            "email": "legaluser@example.com",
            "phone_number": "+998979932945",
            "password": "TestPassword123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('company_name', response.data)
        self.assertEqual(response.data['company_name'][0], "Company name is required for legal entities.")

class CustomTokenObtainPairTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="TestPassword123")

    def test_obtain_token_success(self):
        url = reverse('login')
        data = {
            "username": "testuser",
            "password": "TestPassword123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_obtain_token_invalid_credentials(self):
        url = reverse('token_verify')
        data = {
            "username": "testuser",
            "password": "WrongPassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)