from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User


class TestViewsBasic(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="foo", email="foo@example.com",
                    password="bar")
        self.c = Client()

    def test_index(self):
        """
        Test the homepage
        """
        
        response = self.c.get("/")
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Login")
        self.assertContains(response, "agiliq.com")
