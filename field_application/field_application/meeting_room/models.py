#-*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta, date

from django.utils import timezone
from django.db import models

from field_application.account.models import Organization
from field_application.custom.model_field import MultiSelectField
from field_application.custom.utils import gennerate_date_list_7days 
from field_application.custom.utils import get_applications_a_week 
from field_application.utils.models import get_second_key, get_first_key


def generate_time_table():
    ''' generate TIME for model choices
        ( ('0', '8点-8点30分'),
          ('1', '8点30分-9点'),
          ...
          ('29', '22点30分-23点'),
        )
    '''
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
    deleted = models.BooleanField(default=False)


    @classmethod
    def generate_table(cls, offset=0):
        ''' generate table
        table - date : [ 7 * date ]
              - time_list : [ 30 * time ]
              - content - 石头坞一楼会议室      : [ 7*[ 30*app ] ]
                        - 石头坞二楼会议室      : [ 7*[ 30*app ] ] 
                        - 学生活动中心305会议室 : [ 7*[ 30*app ] ] 
                        - 学生活动中心307会议室 : [ 7*[ 30*app ] ] 
        '''
        content = { place: \
                    [ [None for s, f in cls.TIME] \
                        for j in range(7)] \
                    for short_name, place in cls.PLACE}
        apps_whose_field_used_within_7days \
            = get_applications_a_week(cls, offset)
        today = date.today() + timedelta(days=offset*7)
        for app in apps_whose_field_used_within_7days:
            for t in app.time:
                content[get_second_key(app.place, cls.PLACE)] \
                       [(app.date-today).days][int(t)] = app
        return {'date': gennerate_date_list_7days(offset),
                'time_list': tuple(full_name for s, full_name in cls.TIME),
                'content': content}
