# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Event)
admin.site.register(OrganisedEvent)
admin.site.register(Certificate)
admin.site.register(UserType)
admin.site.register(UserCertificateInfo)




