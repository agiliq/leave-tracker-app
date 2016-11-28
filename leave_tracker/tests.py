from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.core import mail
from django.conf import settings

import datetime
from datetime import timedelta

from .models import LeaveCategory, LeaveApplication, UserProfile
from .admin import approve_multiple


class TestViewsBasic(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="foo",
                                             email="foo@example.com",
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
        start_date = datetime.datetime.now().date() + datetime.timedelta(1)
        end_date = (start_date + datetime.timedelta(1))
        data = {"start_date": start_date, "end_date": end_date,
                "leave_category": cat.pk, "subject": "Going to Timbaktu"
                }
        r = self.c.post("/apply/", data)
        staff_count = User.objects.filter(is_staff=True).count()
        self.assertEqual(LeaveApplication.objects.get(
            subject="Going to Timbaktu").leave_category, cat)
        # Mail goes to all staff, and user foo
        self.assertEqual(len(mail.outbox), staff_count + 1)
        self.assertEqual(mail.outbox[-1].from_email,
                         settings.LEAVE_TRACKER_FROM_MAIL)

    def test_list_page(self):
        "All the leaves list page"
        self.admin = User.objects.create_superuser(username="admin",
                                                   email="admin@example.com",
                                                   password="admin")
        response = self.c.get("/all/")
        self.assertEqual(302, response.status_code)
        self.c.login(username="foo", password="bar")
        response = self.c.get("/all/")
        self.assertEqual(404, response.status_code)
        self.c.login(username="admin", password="admin")
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
        self.user = User.objects.create_user(username="foo",
                                             email="foo@example.com",
                                             password="bar",)
        self.user.first_name = "Luke"
        self.user.save()
        self.category = LeaveCategory.objects.create(type_of_leave="Personal",
                                                     number_of_days=10)
        self.profile = UserProfile.objects.get(user=self.user)
        self.staff_count = User.objects.filter(is_staff=True).count()

    def test_create_leave_application(self):
        start_date = datetime.datetime.now() + datetime.timedelta(1)
        end_date = start_date + datetime.timedelta(1)
        data = {"start_date": start_date, "end_date": end_date,
                "leave_category": self.category, "subject":
                "Going to Timbaktu",
                "usr": self.profile, "status": False
                }
        leave = LeaveApplication.objects.create(**data)

        # Mail goes to all staff, and user foo
        self.assertEqual(len(mail.outbox),
                         self.staff_count + 1)

        last_email = mail.outbox[-1]
        self.assertTrue(self.user.first_name in last_email.body)
        self.assertTrue("requested" in last_email.body)
        self.assertEqual(leave.status_display, "Requested")

    def test_leave_applications_num_of_days(self):
        start = datetime.datetime.now() + datetime.timedelta(1)
        end = start + datetime.timedelta(10)
        data = {"start_date": start, "end_date": end,
                "leave_category": self.category, "subject":
                "Going to Timbaktu",
                "usr": self.profile, "status": False
                }
        leave = LeaveApplication.objects.create(**data)

        holidays = settings.WEEKEND_HOLIDAYS
        dg = (start + timedelta(x + 1) for x in xrange((end - start).days))
        s = sum(1 for day in dg if day.weekday() not in holidays)
        if start.weekday() < 5:
            s += 1

        self.assertEqual(leave.num_of_days, s)

    def test_leave_applications_approval(self):
        start_date = datetime.datetime.now() + datetime.timedelta(1)
        end_date = start_date + datetime.timedelta(1)
        data = {"start_date": start_date, "end_date": end_date,
                "leave_category": self.category,
                "subject": "Going to Timbaktu",
                "usr": self.profile, "status": False
                }
        leave = LeaveApplication.objects.create(**data)
        old_count = len(mail.outbox)
        leave.status = True
        leave.save()
        self.assertEqual(mail.outbox[-1].from_email,
                         settings.LEAVE_TRACKER_FROM_MAIL)
        self.assertEqual(len(mail.outbox), self.staff_count + old_count + 1)
        last_email = mail.outbox[-1]
        self.assertTrue(self.user.first_name in last_email.body)
        self.assertTrue("approved" in last_email.body)
        self.assertEqual(leave.status_display, "Approved")

    def test_admin_approve_multiple(self):
        "The approve multiple admin action"
        start_date = datetime.datetime.now() + datetime.timedelta(1)
        end_date = start_date + datetime.timedelta(1)
        data = {"start_date": start_date, "end_date": end_date,
                "leave_category": self.category,
                "subject": "Going to Timbaktu",
                "usr": self.profile, "status": False
                }
        LeaveApplication.objects.create(**data)
        queryset = LeaveApplication.objects.filter(status=False)
        old_count = len(mail.outbox)
        approve_multiple(None, None, queryset)
        self.assertEqual(LeaveApplication.objects.filter
                         (status=False).count(), 0)
        self.assertEqual(len(mail.outbox), self.staff_count + old_count + 1)

    def test_duplicated_username(self):
        "If you try to create two users with same username, it gets a suffix"
        User.objects.create(username="dup", password="bar")
        User.objects.create(username="dup", password="bar")
        self.assertEqual(User.objects.filter(username="dup").count(), 1)
        self.assertEqual(User.objects.filter(username="dup2").count(), 1)

    def test_username_does_not_change(self):
        "Username should not change on multiple logins"
        c = Client()
        u1 = User.objects.create_user(username="dup", password="bar")
        c.login(username="dup", password="bar")
        c.logout()
        u2 = User.objects.create_user(username="dup", password="bar")
        c.login(username="dup", password="bar")
        c.logout()
        c.login(username="dup2", password="bar")
        c.logout()
        self.assertEqual(User.objects.filter(username="dup").count(), 1)
        self.assertEqual(User.objects.filter(username="dup2").count(), 1)
