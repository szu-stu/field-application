#-*- coding: utf-8 -*-
import copy
from datetime import datetime, timedelta

from django.utils import timezone
from django.db import models

from field_application.account.models import Organization
from field_application.custom.utils import gennerate_date_list_7days 
from field_application.custom.utils import get_applications_a_week 
from field_application.utils.models import file_save_path
from field_application.utils.models import get_second_key


class StudentActivityCenterApplication(models.Model):

    PLACE = (
        ('Square', u'学生活动中心前广场'),
        ('LectureHall', u'一楼影视报告厅'),
        ('3rdFloorEast', u'学生活动中心三楼天台(东)'),
        ('3rdFloorWest', u'学生活动中心三楼天台(西)'),
        ('TheStoneDock', u'石头坞广场'),
    )
    TIME = (
        ('MOR', u'早上'),
        ('AFT', u'下午'),
        ('EVE', u'晚上'),
    )

    organization = models.ForeignKey(Organization)
    place = models.CharField(max_length=20, choices=PLACE)
    date = models.DateField()
    time = models.CharField(max_length=10, choices=TIME)
    activity = models.CharField(max_length=30)
    approved = models.BooleanField(default=False)
    application_time = models.DateTimeField(auto_now_add=True)
    plan_file = models.FileField(
            upload_to=file_save_path('student_activity_center'))

    applicant_name = models.CharField(max_length=10)
    applicant_phone_number = models.CharField(max_length=30)
    activity_summary = models.CharField(max_length=200)
    sponsor = models.CharField(max_length=30, blank=True, null=True)
    sponsorship = models.CharField(max_length=30, blank=True, null=True)
    sponsorship_usage = models.CharField(max_length=40, blank=True, null=True)

    @classmethod
    def generate_table(cls, offset=0):
        ''' generate dict
        table-date : [ 7 * date ] 
             -学生活动中心前广场      : [7 * {'MOR': [], 'AFT': [], 'EVE': []} ]
             -一楼影视报告厅          : [7 * {'MOR': [], 'AFT': [], 'EVE': []} ]
             -学生活动中心三楼天台(东): [7 * {'MOR': [], 'AFT': [], 'EVE': []} ]
             -学生活动中心三楼天台(西): [7 * {'MOR': [], 'AFT': [], 'EVE': []} ]
             -石头坞广场              : [7 * {'MOR': [], 'AFT': [], 'EVE': []} ]
        '''
        field_used_this_week_applications = \
                get_applications_a_week(cls, offset)
        table = {}
        empty_time_dict = { time: [] for time, l in cls.TIME }
        for short_name, full_name in cls.PLACE:
            table[full_name] = [copy.deepcopy(empty_time_dict) for i in range(7)]
            apps = field_used_this_week_applications.filter(place=short_name)
            for app in apps:
                if app.time in empty_time_dict:
                    table[full_name][app.date.weekday()][app.time].append(app)
                else:
                    raise Exception('invalid time')
        table['date'] = gennerate_date_list_7days(offset)
        return table
