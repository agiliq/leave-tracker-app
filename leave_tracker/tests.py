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
        Homepage returns a http 200 and has the basic text
        """
        
        response = self.c.get("/")
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Login")
        self.assertContains(response, "agiliq.com")

    def test_apply_page(self):
        "Apply page is available only after loggin in"
        response = self.c.get("/apply/")
        self.assertEqual(302, response.status_code)
        self.c.login(username="foo", password="bar")
        response = self.c.get("/apply/")
        self.assertEqual(200, response.status_code)

    def test_list_page(self):
        "All the leaves list page"
        response = self.c.get("/all/")
        self.assertEqual(302, response.status_code)
        self.c.login(username="foo", password="bar")
        response = self.c.get("/all/")
        self.assertEqual(200, response.status_code)

    def test_personal_leaves_page(self):
        "Your leaves list page"
        response = self.c.get("/personal/")
        self.assertEqual(302, response.status_code)
        self.c.login(username="foo", password="bar")
        response = self.c.get("/personal/")
        self.assertEqual(200, response.status_code)






class TestModel(TestCase):
    pass
