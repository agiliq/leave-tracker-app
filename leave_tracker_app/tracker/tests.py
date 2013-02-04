"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test import Client


class TestViewsBasic(TestCase):
    def test_index(self):
        """
        Test the homepage
        """
        c = Client()
        response = c.get("/")
        self.assertEqual(200, response.status_code)
