from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from shop_app.models import User

User = get_user_model()

class UserCRUDTestCase(APITestCase):

    def setUp(self):
      # 1. Delete existing user if it exists
        User.objects.filter(username='test_admin_unique_4').delete()
        User.objects.filter(email='test_admin4@example.com').delete()

      # 2. Create new user
        self.user = User.objects.create_user(
            username='test_admin_unique_2',
            password='Pass@123',
            email='test_admin2@example.com',
            role='admin'
        )

       # 3. Get JWT token
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'test_admin_unique_2',
            'password': 'Pass@123'
        }, format='json')

        # 4. Authenticate client with Bearer token
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # 5. Common user data for create tests
        self.create_url = reverse('user-list')
        self.user_data = {'username': 'test_user_unique','password':'Pass@123','email':'test_user@example.com','role': 'user'}

    def test_create_user(self):
        response = self.client.post(self.create_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_list_users(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_retrive_user(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        
    def test_update_user(self):
        url = reverse('user-detail', args=[self.user.id])
        data = {'username': 'test_admin_unique_new', 'password':'Pass@123','email':'test_user@example.com','role': 'user'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_user(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 

        