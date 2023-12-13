from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import PurchaseOrder, Vendor
from datetime import datetime, timedelta, timezone

class OrderApiTests(TestCase):
    """
    Does the setup for running the tests.
    """
    def setUp(self):
        # Create a user and obtain a token
        self.user = User.objects.create_user(username='user', password='pass123')
        self.client = APIClient()
        self.token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.vendor = Vendor.objects.create(name='Test Vendor', 
                                            contact_details='9456789199',
                                            address='111 New Jersey, 21254',
                                            vendor_code="1")
        self.purchase_order = PurchaseOrder.objects.create(
            po_number='PO1',
            order_date=datetime.now(timezone.utc),
            delivery_date=datetime.now(timezone.utc) + timedelta(days=15),
            items={'item1': 1, 'item2': 2},
            quantity=3,
            status='pending',
            issue_date=datetime.now(timezone.utc) + timedelta(minutes=3),
            vendor=self.vendor
        )

    """
    Creates the token for authentication.

    Returns:
        string: The token value.
    """
    def get_token(self):
        response = self.client.post('/auth/login/', {'username': 'user', 'password': 'pass123'})
        return response.data['token']

    """
    Tests the POST request to /api/purchase_orders/ to add new purchase orders.
    """
    def test_order_details_post(self):
        data = {
            'po_number': 'PO2',
            'order_date': datetime.now(timezone.utc),
            'delivery_date': datetime.now(timezone.utc) + timedelta(days=15),
            'items': {'item3': 1, 'item4': 2},
            'quantity': 3,
            'status': 'pending',
            'issue_date': datetime.now(timezone.utc) + timedelta(minutes=3),
            'vendor': self.vendor.vendor_id
        }
        response = self.client.post('/api/purchase_orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    """
    Tests the GET request to /api/purchase_orders/ to get details of all purchase orders.
    """
    def test_order_details_get(self):
        response = self.client.get('/api/purchase_orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """
    Tests the PUT request to /api/purchase_orders/po_id to update details of a specific purchase order.
    """
    def test_order_put(self):
        data = {'status': 'completed'}
        response = self.client.put(f'/api/purchase_orders/{self.purchase_order.po_id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.status, 'completed')

    """
    Tests the DELETE request to /api/purchase_orders/po_id to delete details of a specific purchase order.
    """
    def test_order_delete(self):
        response = self.client.delete(f'/api/purchase_orders/{self.purchase_order.po_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    """
    Tests the POST request to /api/purchase_orders/po_id/acknowledge to post acknowledgement for a specific order.
    """
    def test_acknowledge_post(self):
        response = self.client.post(f'/api/purchase_orders/{self.purchase_order.po_id}/acknowledge/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

