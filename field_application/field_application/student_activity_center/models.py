#-*- coding: utf-8 -*-
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

    organization = models.OneToOneField(Organization)
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


