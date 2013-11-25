#-*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta

from django.utils import timezone
from django.db import models

from field_application.account.models import Organization
from field_application.custom.model_field import MultiSelectField
from field_application.custom.utils import generate_date_list_this_week
from field_application.custom.utils import get_applications_a_week 


def file_save_path(instance, filename):
    path = 'south_stadium'
    path = os.path.join(path, instance.organization.user.username)
    return os.path.join(path, instance.activity + '_' + filename)

class SouthStadiumApplication(models.Model):

    TIME = (
        ('MOR', u'早上08:00-12:00'),
        ('AFT', u'下午14:00-17:00'),
        ('EVE', u'晚上19:00-22:30'),
    )

    organization = models.ForeignKey(Organization)
    date = models.DateField()
    time = MultiSelectField(max_length=10, choices=TIME)
    activity = models.CharField(max_length=30)
    approved = models.BooleanField(default=False)
    application_time = models.DateTimeField(auto_now_add=True)

    plan_file = models.FileField(upload_to=file_save_path, blank=True, null=True)
    applicant_name = models.CharField(max_length=10)
    applicant_phone_number = models.CharField(max_length=30)
    activity_summary = models.CharField(max_length=200)
    sponsor = models.CharField(max_length=30, blank=True, null=True)
    sponsorship = models.CharField(max_length=30, blank=True, null=True)
    sponsorship_usage = models.CharField(max_length=40, blank=True, null=True)
    remarks = models.CharField(max_length=300, blank=True, null=True)

    @classmethod
    def generate_table(cls, offset=0):
        apps_whose_field_used_within_7days \
            = get_applications_a_week(cls, offset)
        table = {}
        for time_short_name, time_full_name in cls.TIME:
            table[time_full_name] = []
            for i in range(0, 7):
                table[time_full_name].append(None)
            for app in apps_whose_field_used_within_7days:
                table[time_full_name][app.date.weekday()] = app
        table['date'] = generate_date_list_this_week()
        return table
