# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

from .functions import *
from .models import *
from django.test import TestCase

# Create your tests here.
class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(add_user(), 4)