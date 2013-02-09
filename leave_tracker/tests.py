from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core import mail
from django.conf import settings

import datetime

from .models import LeaveCategory, LeaveApplication, UserProfile
from .admin import approve_multiple


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

    def test_apply(self):
        self.c.login(username="foo", password="bar")
        cat = LeaveCategory.objects.create(type_of_leave="Personal", 
                        number_of_days=10)
        data = {"start_date": "02/07/2013", "end_date": "02/07/2013",
                "leave_category": cat.pk, "subject": "Going to Timbaktu"
            }
        self.c.post("/apply/", data)
        staff_count=User.objects.filter(is_staff=True).count()
        self.assertEqual(LeaveApplication.objects.get(subject=
                        "Going to Timbaktu").leave_category, cat)
        self.assertEqual(len(mail.outbox), staff_count+1)#Mail goes to all staff, and user foo
        self.assertEqual(mail.outbox[-1].from_email, settings.DEFAULT_FROM_EMAIL)

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
    def setUp(self):
        self.user = User.objects.create_user(username="foo", email="foo@example.com",
                    password="bar",)
        self.user.first_name = "Luke"
        self.user.save()
        self.category = LeaveCategory.objects.create(type_of_leave="Personal", 
                        number_of_days=10)
        self.profile = UserProfile.objects.get(user=self.user)
        self.staff_count=User.objects.filter(is_staff=True).count()
    
    def test_create_leave_application(self):
        
        import datetime
        today=datetime.date.today()
        tomorrow=datetime.date.today()+datetime.timedelta(1)
        data = {"start_date": today, "end_date": tomorrow,
                "leave_category": self.category, "subject": "Going to Timbaktu",
                "usr": self.profile, "status": False
            }
        LeaveApplication.objects.create(**data)
        
        self.assertEqual(len(mail.outbox),
                self.staff_count+1)#Mail goes to all staff, and user foo
        last_email = mail.outbox[-1]
        self.assertTrue(self.user.first_name in last_email.body)


    def test_leave_applications_approval(self):
        today=datetime.date.today()
        tomorrow=datetime.date.today()+datetime.timedelta(1)
        data = {"start_date": today, "end_date": tomorrow,
                "leave_category": self.category, "subject": "Going to Timbaktu",
                "usr": self.profile, "status": False
            }
        leave_application = LeaveApplication.objects.create(**data)
        old_count = len(mail.outbox)
        leave_application.status = True
        leave_application.save()
        self.assertEqual(mail.outbox[-1].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(len(mail.outbox), self.staff_count+old_count+1)

    def test_admin_approve_multiple(self):
        "The approve multiple admin action"
        today=datetime.date.today()
        tomorrow=datetime.date.today()+datetime.timedelta(1)
        data = {"start_date": today, "end_date": tomorrow,
                "leave_category": self.category, "subject": "Going to Timbaktu",
                "usr": self.profile, "status": False
            }
        leave_application = LeaveApplication.objects.create(**data)
        queryset = LeaveApplication.objects.filter(status=False)
        old_count = len(mail.outbox)
        approve_multiple(None, None, queryset)
        self.assertEqual(LeaveApplication.objects.filter(status=False).count(), 0)
        self.assertEqual(len(mail.outbox), self.staff_count+old_count+1)

        



