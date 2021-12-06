from django.test import TestCase
from rest_framework.test import APIClient 
from rest_framework import status 
from django.core.urlresolvers import reverse 
# Create your tests here.

class ViewTestCase(TestCase):
    def setUp(self): 
        self.client = APIClient() 
        self.req_data = { 'str_numbers': '1,2'}
        self.response = self.client.post(reverse('create'), self.req_data, format = 'json') 

    def test_api_canADD(self): 
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_getView(self):  
        response = self.client.post( 'calculator', { 'str_numbers': '3,2'} , format = 'json')
        self.assertEqual(response, 5)