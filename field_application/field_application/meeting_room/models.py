#-*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta

from django.utils import timezone
from django.db import models

from field_application.account.models import Organization
from field_application.custom.model_field import MultiSelectField


def generate_time_table():
    ''' generate TIME for model choices '''
    start = 8
    end = 8
    time_table = []
    for i in range(0, 30):
        if not i%2:
            time_table.append((str(i), str(start) + u'点-' + str(end) + u'点30分'))
            end += 1
        else:
            time_table.append((str(i), str(start) + u'点30分-' + str(end) + u'点'))
            start += 1
    return time_table


def file_save_path(instance, filename):
    path = 'meeting_room'
    path = os.path.join(path, instance.organization.user.username)
    return os.path.join(path, instance.activity + '_' + filename)


class MeetingRoomApplication(models.Model):

    TIME = generate_time_table()

    PLACE = (
        ('1F', u'石头坞一楼会议室'),
        ('2F', u'石头坞二楼会议室'),
        ('305', u'学生活动中心305会议室'),
        ('307', u'学生活动中心307会议室'),
    )

    meeting_topic = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization)
    date = models.DateField()
    place = models.CharField(max_length=200, choices=PLACE)
    time = MultiSelectField(max_length=15, choices=TIME)
    applicant_name = models.CharField(max_length=10)
    applicant_phone_number = models.CharField(max_length=30)
    meeting_summary = models.CharField(max_length=200)
    remarks = models.CharField(max_length=300, blank=True, null=True)
    approved = models.BooleanField(default=False)
    application_time = models.DateTimeField(auto_now_add=True)

