#-*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta

from django.utils import timezone
from django.db import models

from field_application.account.models import Organization
from field_application.custom.model_field import MultiSelectField


def file_save_path(instance, filename):
    path = 'campus_field'
    path = os.path.join(path, instance.organization.user.username)
    return os.path.join(path, instance.activity + '_' + filename)


class CampusFieldApplication(models.Model):

    organization = models.ForeignKey(Organization)
    start_date = models.DateField()
    end_date = models.DateField()
    activity = models.CharField(max_length=30)
    approved = models.BooleanField(default=False)
    application_time = models.DateTimeField(auto_now_add=True)

    plan_file = models.FileField(upload_to=file_save_path)
    applicant_name = models.CharField(max_length=10)
    applicant_phone_number = models.CharField(max_length=30)
    activity_summary = models.CharField(max_length=200)
    sponsor = models.CharField(max_length=30, blank=True, null=True)
    sponsorship = models.CharField(max_length=30, blank=True, null=True)
    sponsorship_usage = models.CharField(max_length=40, blank=True, null=True)
    remarks = models.CharField(max_length=300, blank=True, null=True)


class ExhibitApplication(CampusFieldApplication):

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
    )

    EXHIBITION = (
        ('OTH', u'other'),
        ('PIC', u'picture'),
        ('POS', u'poster'),
    )

    #place = models.CharField(max_length=200, choices=PLACE)
    place = MultiSelectField(max_length=200, choices=PLACE)
    time = MultiSelectField(max_length=10, choices=TIME)
    exhibition = models.CharField(max_length=20, choices=EXHIBITION)
    other_exhibition = models.CharField(max_length=20,
                                        blank=True, null=True)
    exhibit_board_number = models.IntegerField()
    

class PublicityApplication(CampusFieldApplication):

    PLACE = (
        ('Square', '学生活动中心前广场'),
        ('LectureHall', '一楼影视报告厅'),
        ('3rdFloorEast', '学生活动中心三楼天台(东)'),
        ('3rdFloorWest', '学生活动中心三楼天台(西)'),
        ('TheStoneDock', '石头坞广场'),
    )
   
    TIME = (
        ('p1', '8-9'),
        ('P2', '8-9'),
        ('P3', '8-9'),
        ('P4', '8-9'),
        ('P5', '8-9'),
        ('P6', '8-9'),
        ('P7', '8-9'),
        ('P8', '8-9'),
        ('P9', '8-9'),
        ('P1', '8-9'),
        ('P1', '8-9'),
    )

    ACTIVITY_TYPE = (
        ('LEAFLET', 'deliver leaflet'),
        ('STAND', 'set stand'),
    )

    activity_type = models.CharField(max_length=10, choices=ACTIVITY_TYPE)
    other_activity_type = models.CharField(max_length=10,
                                           blank=True, null=True)
    place = models.CharField(max_length=200)
    time = models.CharField(max_length=5, choices=TIME)

