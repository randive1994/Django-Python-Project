from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from shop_app.models import User, Book

User = get_user_model()

class BookCRUDTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
      # 1. Delete existing user if it exists
        User.objects.filter(username='test_admin_unique_4').delete()
        User.objects.filter(email='test_admin4@example.com').delete()

      # 2. Create new user
        cls.user = User.objects.create_user(
            username='test_admin_unique_2',
            password='Pass@123',
            email='test_admin2@example.com',
            role='admin'
        )

        # Generate token using the user object
        refresh = RefreshToken.for_user(cls.user)
        cls.access_token = str(refresh.access_token)

        # 5.Book data for create tests
        cls.create_url = reverse('book-list')
        cls.book_data1 = {
            "title": "Shared Book",
            "author": "Author Z",
            "published_date": "2024-05-01",
            "price": 100.00
        }
        response = Book.objects.create(**cls.book_data1)
        cls.book_id = response.id   # available to all test methods
        cls.book_data = {'title': 'Gitanjali','author':'Rabindranath Tagore','published_date':'2025-06-10','price': 120}
  
    def setUp(self):
        # Set the Authorization header for all requests in this test
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
                
    def test_create_book(self):
        response = self.client.post(self.create_url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_list_books(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_retrive_book(self):
        url = reverse('book-detail', args=[self.book_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        
    def test_update_book(self):
        url = reverse('book-detail', args=[self.book_id])
        data = {'title': 'Gitanjali','author':'Rabindranath Tagore','published_date':'2025-06-10','price': 122}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_book(self):
        url = reverse('book-detail', args=[self.book_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 

        