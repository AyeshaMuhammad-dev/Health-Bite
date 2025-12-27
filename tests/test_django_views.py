"""
Unit tests for Django views and endpoints.
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from core_app.models import Food, DietPlan, Workout
import json

User = get_user_model()


class UserRegistrationTests(TestCase):
    """Tests for user registration."""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
    
    def test_user_registration_success(self):
        """Test successful user registration."""
        data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'testpass123',
            'password2': 'testpass123',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('tokens', response.data)
        self.assertEqual(response.data['user']['email'], 'test@example.com')
    
    def test_user_registration_password_mismatch(self):
        """Test registration with mismatched passwords."""
        data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'testpass123',
            'password2': 'differentpass',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTests(TestCase):
    """Tests for user login."""
    
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
    
    def test_user_login_success(self):
        """Test successful user login."""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123',
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
    
    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class FoodLoggingTests(TestCase):
    """Tests for food logging endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_food_entry(self):
        """Test creating a food log entry."""
        url = reverse('food-list')
        data = {
            'name': 'Grilled Chicken',
            'calories': 231,
            'nutrients': {
                'protein': 43.5,
                'carbs': 0,
                'fats': 5,
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Food.objects.count(), 1)
        self.assertEqual(Food.objects.get().name, 'Grilled Chicken')
    
    def test_list_food_entries(self):
        """Test listing user's food entries."""
        Food.objects.create(
            user=self.user,
            name='Apple',
            calories=52
        )
        url = reverse('food-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class AnalyticsTests(TestCase):
    """Tests for analytics endpoint."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_analytics_endpoint(self):
        """Test analytics endpoint returns data."""
        # Create some food entries
        Food.objects.create(
            user=self.user,
            name='Apple',
            calories=52,
            nutrients={'protein': 0.3, 'carbs': 14}
        )
        Food.objects.create(
            user=self.user,
            name='Banana',
            calories=89,
            nutrients={'protein': 1.1, 'carbs': 23}
        )
        
        url = reverse('analytics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_calories', response.data)
        self.assertIn('average_calories_per_day', response.data)
