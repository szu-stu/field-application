#-*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta, date

from django.db import models

from field_application.account.models import Organization
from field_application.custom.model_field import MultiSelectField
from field_application.custom.utils import gennerate_date_list_7days 
from field_application.custom.utils import get_applications_a_week 
from field_application.utils.models import get_second_key, get_first_key
from field_application.custom.validators import validate_file_extension


def generate_time_table():
    ''' generate TIME for model choices
        ( ('8点-8点30分', '8点-8点30分'),
          ('8点30分-9点', '8点30分-9点'),
          ...
          ('22点30分-23点', '22点30分-23点'),
        )
    '''
    s = [8, u'点', 8, u'点30分']
    TIME = []
    for i in range(30):
        x, a, y, b = s
        t = str(x)+a + '-' + str(y)+b
        TIME.append((t, t))
        s = [y, b, x+1, a]
    return TIME


class InteServiceApplication(models.Model):

    TIME = generate_time_table()

    PLACE = (
        (u'一楼 101活动室', u'一楼 101活动室'),
        (u'一楼 111工作坊', u'一楼 111工作坊'),
        (u'一楼 110工作坊', u'一楼 110工作坊'),
        (u'四楼 426会议室', u'四楼 426会议室'),
        (u'一楼 中厅', u'一楼 中厅'),
        #(u'天台', u'天台'),
    )

    topic = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization)
    date = models.DateField()
    place = models.CharField(max_length=50, choices=PLACE)
    # 如果多选的时候，最高要存30个时间，所以这里开到400
    time = MultiSelectField(max_length=400, choices=TIME)
    applicant_name = models.CharField(max_length=10)
    applicant_stu_id = models.CharField(max_length=15)
    applicant_college = models.CharField(max_length=50)
    applicant_phone_number = models.CharField(max_length=30)
    summary = models.CharField(max_length=200)
    remarks = models.CharField(max_length=300, blank=True, null=True)
    approved = models.BooleanField(default=False)
    application_time = models.DateTimeField(auto_now_add=True)
    sponsor = models.CharField(max_length=30, blank=True, null=True)
    sponsorship = models.CharField(max_length=30, blank=True, null=True)
    sponsorship_usage = models.CharField(max_length=40, blank=True, null=True)
    deleted = models.BooleanField(default=False)


    @classmethod
    def generate_table(cls, offset=0):

        content = { place: [ {time: [] for time, t in cls.TIME} \
                        for j in range(7)] \
                    for place, p in cls.PLACE}
        apps_whose_field_used_within_7days \
            = get_applications_a_week(cls, offset)
        first_day = date.today() + timedelta(days=offset*7)
        for app in apps_whose_field_used_within_7days:
            for t in app.time:
                content[app.place][(app.date-first_day).days][t].append(app)
        # sort in the order of TIME
        for place in content:
            for day in range(7):
                content[place][day] = [content[place][day][time] \
                                        for time, t in cls.TIME ]
        # sort int the order of PLACE
        content = [(place, content[place]) for place, p in cls.PLACE]
        return {'date': gennerate_date_list_7days(offset),
                'time_list': tuple(time for time, t in cls.TIME),
                'content': content}
