from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor

class VendorApiTests(TestCase):
    """
    Does the setup for running the tests.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass123')
        self.client = APIClient()
        self.token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.vendor = Vendor.objects.create(name='Test Vendor', 
                                            contact_details='9456789199',
                                            address='111 New Jersey, 21254',
                                            vendor_code="1")

    """
    Creates the token for authentication.

    Returns:
        string: The token value.
    """
    def get_token(self):
        response = self.client.post('/auth/login/', {'username': 'user', 'password': 'pass123'})
        return response.data['token']

    """
    Tests the POST request to /api/vendors/ to add new vendors.
    """
    def test_vendor_details_post(self):
        data = {
                "name": "Real Vendors",
                "contact_details": "9999999999",
                "address": "123 New Jersey, 21654",
                "vendor_code": "6"
            }
        response = self.client.post('/api/vendors/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    """
    Tests the GET request to /api/vendors/ to get details of all vendors.
    """
    def test_vendor_details_get(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """
    Tests the GET request to /api/vendors/ to get details of a specific vendor.
    """
    def test_vendor_details_get_vendor(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get(f'/api/vendors/{self.vendor.vendor_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("vendor_id"), self.vendor.vendor_id)

    """
    Tests the PUT request to /api/vendors/vendor_id to update the details of a specific vendor.
    """
    def test_vendor_put(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        data = {'contact_details': '9823456711'}
        response = self.client.put(f'/api/vendors/{self.vendor.vendor_id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """
    Tests the DELETE request to /api/vendors/vendor_id to delete the details of a specific vendor.
    """
    def test_vendor_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.delete(f'/api/vendors/{self.vendor.vendor_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    """
    Tests the GET request to /api/vendors/vendor_id/performance to get the performance of a specific vendor.
    """
    def test_vendor_performance_get(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get(f'/api/vendors/{self.vendor.vendor_id}/performance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

