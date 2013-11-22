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
        ('CD', u'CD座文化长廊'),
        ('A', u'A座文化大厅'),
        ('SW', u'西南餐厅前空地'),
        ('LS', u'荔山餐厅前空地'),
    )
    
    TIME = (
        ('MOR', u'早上'),
        ('AFT', u'下午'),
    )

    EXHIBITION = (
        ('OTH', u'其它'),
        ('PIC', u'图片'),
        ('POS', u'海报'),
    )

    place = MultiSelectField(max_length=200, choices=PLACE)
    time = MultiSelectField(max_length=10, choices=TIME)
    exhibition = models.CharField(max_length=20, choices=EXHIBITION)
    other_exhibition = models.CharField(max_length=20,
                                        blank=True, null=True)
    exhibit_board_number = models.IntegerField()
    

class PublicityApplication(CampusFieldApplication):

    PLACE = (
        ('', u'荔山餐厅前空地'),
        ('', u'西南餐厅前空地'),
        ('', u'文山湖路口'),
        ('', u'桂庙路口'),
        ('CD', u'CD座文化长廊'),
        ('A', u'A座文化大厅'),
    )
   
    TIME = (
        (8, '8点-9点'),
        (9, '9点-10点'),
        (10, '10点-11点'),
        (11, '11点-12点'),
        (12, '12点-13点'),
        (13, '13点-14点'),
        (14, '14点-15点'),
        (15, '15点-16点'),
        (16, '16点-17点'),
        (17, '17点-18点'),
        (18, '18点-19点'),
    )

    ACTIVITY_TYPE = (
        ('LEAFLET', '派传单'),
        ('STAND', '设点'),
        ('OTHER', '其它'),
    )

    activity_type = models.CharField(max_length=10, choices=ACTIVITY_TYPE)
    other_activity_type = models.CharField(max_length=10,
                                           blank=True, null=True)
    place = MultiSelectField(max_length=200)
    time = models.CharField(max_length=5, choices=TIME)

