import os
from datetime import datetime, timedelta

from django.utils import timezone
from django.db import models
from field_application.account.models import Organization


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
    place = models.CharField(max_length=40)


class ExhibitApplication(CampusFieldApplication):
    
    TIME = (
        ('MOR','早上'),
        ('AFT','下午'),
    )

    exhibition = models.CharField(max_length=20)
    exhibit_board_number = models.IntegerField()
    time = models.CharField(max_length=10, choice=TIME)
    

class PublicityApplication(CampusFieldApplication):

    TIME = (
        ('p1','8-9'),
        ('P2','8-9'),
        ('P3','8-9'),
        ('P4','8-9'),
        ('P5','8-9'),
        ('P6','8-9'),
        ('P7','8-9'),
        ('P8','8-9'),
        ('P9','8-9'),
        ('P1','8-9'),
        ('P1','8-9'),
    )

    time = models.CharField(max_length=5, choice=TIME)

