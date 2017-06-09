# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import *
from .functions import *


class Test(TestCase):

    def test_addUser(self):
        user = add_user("user", "user", "user", "user", "user@mp.com", "2016-08-03", "abc")
        user1 = User.objects.get(username="user")
        self.assertEqual(user, user1)

    def test_addCertificate(self):
        path = settings.MEDIA_ROOT
        file = os.path.join(path, "assignment_2.pdf")
        certificate = add_certificate(file, "test_title")
        certificate1 = Certificate.objects.get(title="test_title")
        self.assertEqual(certificate, certificate1)

    def test_createEvent(self):
        event = create_event("test", certificate=Certificate(), user=User())
        event1 = Event.objects.get(name="test")
        self.assertEqual(event,event1)

