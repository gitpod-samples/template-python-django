from django.test import TestCase

# Create your tests here.

class URLTests(TestCase):

    def test_todo_app_ok(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_todo_app_notok(self):
            response = self.client.get('/MyCoffee')
            self.assertEqual(response.status_code, 404)
        
