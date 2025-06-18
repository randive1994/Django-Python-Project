from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from shop_app.models import User, Product

User = get_user_model()

class ProductCRUDTestCase(APITestCase):

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

        # 5.Product data for create tests
        cls.create_url = reverse('product-list')
        cls.product_data1 = {
            "name": "AC",
            "description": "LG",
            "stock": 2,
            "price": 100,
            "sku":"Test-SKU"
        }
        response = Product.objects.create(**cls.product_data1)
        
        cls.product_id = response.id  # available to all test methods
        cls.product_data = { "name": "TV","description": "Samsung","stock": 20,'price': 800000,"sku":"Test-SKU-0"}
        
    def setUp(self):
         # Set the Authorization header for all requests in this test
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        
    def test_create_product(self):
        response = self.client.post(self.create_url, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_list_products(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_retrive_product(self):
        url = reverse('product-detail', args=[self.product_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        
    def test_update_product(self):
        url = reverse('product-detail', args=[self.product_id])
        data = { "name": "TV","description": "Samsung","stock": 20,'price': 900000,"sku":"Test-SKU1"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_product(self):
        url = reverse('product-detail', args=[self.product_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 

        