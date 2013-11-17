#-*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.utils import timezone
from django.db import models
from field_application.account.models import Organization


class StudentActivityCenterApplication(models.Model):

    PLACE = (
        ('Square','学生活动中心前广场'),
        ('LectureHall','一楼影视报告厅'),
        ('3rdFloorEast','学生活动中心三楼天台(东)'),
        ('3rdFloorWest','学生活动中心三楼天台(西)'),
        ('TheStoneDock','石头坞广场'),
    )
    TIME = (
        ('MOR','早上'),
        ('AFT','下午'),
        ('EVE','晚上'),
    )

    organization = models.ForeignKey(Organization)
    place = models.CharField(max_length=20, choices=PLACE)
    date = models.DateField()
    time = models.CharField(max_length=10, choices=TIME)
    activity = models.CharField(max_length=30)
    approved = models.BooleanField(default=False)
    application_time = models.DateTimeField(auto_now_add=True)

    applicant_name = models.CharField(max_length=10)
    applicant_phone_number = models.CharField(max_length=30)
    activity_summary = models.CharField(max_length=200)
    # plan document
    sponsor = models.CharField(max_length=30, blank=True, null=True)
    sponsorship = models.CharField(max_length=30, blank=True, null=True)
    sponsorship_usage = models.CharField(max_length=40, blank=True, null=True)

    @classmethod
    def generate_table(cls):
        field_used_this_week_applications = cls.get_application_this_week()
        table = {}
        for short_name, full_name in cls.PLACE:
            table[short_name] = []
            for i in range(0, 7):
                table[short_name].append([None, None, None])
            apps = field_used_this_week_applications.filter(place=short_name)
            for app in apps:
                if app.time == 'MOR':
                    table[short_name][app.date.weekday()][0] = app
                elif app.time == 'AFT':
                    table[short_name][app.date.weekday()][1] = app
                elif app.time == 'EVE':
                    table[short_name][app.date.weekday()][2] = app
                else:
                    raise Exception('invalid time')
        table['date'] = cls.generate_date_list()
        return table

    @classmethod
    def generate_date_list(cls):
        date_list = []
        now = timezone.now()
        date_of_this_Monday = now - timedelta(days=now.weekday())
        for i in range(0, 7):
            date_list.append(date_of_this_Monday + timedelta(days=i))
        return date_list

    @classmethod
    def get_application_this_week(cls):
        ''' get all applications whose applied field
        is going to be used this week '''
        now = timezone.now()
        date_of_this_Monday = now - timedelta(days=now.weekday())
        date_of_next_Monday = date_of_this_Monday + timedelta(days=7)
        application_this_week = cls.objects.filter(
            date__gte=date_of_this_Monday,
            date__lt=date_of_next_Monday)
        return application_this_week

