# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .functions import *


class TestAddUser(TestCase):

    def test_addUser(self):
        user = add_user_profile("user", "user", "user@mp.com", "2016-08-03", "college", 8763782882)
        user1 = UserProfile.objects.get(email="user@mp.com")
        self.assertEqual(user, user1)
        return user1


class TestAddCertificate(TestCase):

    def test_addCertificate(self):
        certificate = add_certificate("assignment_2.zip", "test_title")
        certificate1 = Certificate.objects.get(title="test_title")
        self.assertEqual(certificate, certificate1)
        return certificate1


class TestEvent(TestCase):

    def setUp(self):
        self.user = UserProfile(first_name="user", last_name="user", email="user@mp.com", dob="2017-08-21", college="abc", contact_number=787673676)
        self.user.save()
        self.certificate = add_certificate("assignment_2.zip", "test_title")
        self.creator=User.objects.create_user(username="user",password="user",email="user@gmail.com",first_name="user",last_name="user")

    def test_createEvent(self):
        event = create_event("test", self.certificate, self.creator)
        event1 = Event.objects.get(name="test")
        self.assertEqual(event, event1)
        return event1

    def test_organiseEvent(self):
        event = self.test_createEvent()
        oe = organise_event(event, datetime.strptime("2017-09-01", "%Y-%m-%d").date(), datetime.strptime("2017-09-03", "%Y-%m-%d").date(), self.creator, "abc", [self.user])
        oe1 = OrganisedEvent.objects.get(event=event)
        self.assertEqual(oe, oe1)


class TestUserCertificateInfo(TestCase):

    def setUp(self):
        self.user = add_user_profile("user", "user", "user@mp.com", "2017-08-21", "user", 7878668889)
        self.certificate = add_certificate("assignment_2.zip", "test_title")
        self.creator = User.objects.create_user(username="user", password="user", email="user@gmail.com",
                                                first_name="user", last_name="user")
        self.event = create_event("test", self.certificate, self.creator)
        self.organised_event = organise_event(self.event, datetime.strptime("2017-09-01", "%Y-%m-%d").date(), datetime.strptime("2017-09-03", "%Y-%m-%d").date(), self.creator, "abc", [self.user])
        user_type = UserType(name="test")
        user_type.save()
        self.user_type=user_type.name


    def test_addUserCertificateInfo(self):
        user_info = add_user_certificate_info(self.user, self.organised_event, [self.user_type])
        user_info1 = UserCertificateInfo.objects.get(user=self.user)
        self.assertEqual(user_info, user_info1)

    def test_qrCode(self):
        self.test_addUserCertificateInfo()
        qrcode = generate_qrcode(self.user, self.organised_event)
        qr1 = UserCertificateInfo.objects.get(user=self.user, organised_event=self.organised_event)
        self.assertEqual(qrcode, qr1.qrcode)
