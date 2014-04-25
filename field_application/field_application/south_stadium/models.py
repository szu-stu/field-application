#-*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta, date

from django.utils import timezone
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from field_application.account.models import Organization
from field_application.custom.model_field import MultiSelectField
from field_application.custom.utils import gennerate_date_list_7days 
from field_application.custom.utils import get_applications_a_week 
from field_application.utils.models import file_save_path
from field_application.utils.models import get_second_key, get_first_key
from field_application.custom.validators import validate_file_extension


class SouthStadiumApplication(models.Model):

    TIME = (
        (u'早上08:00-12:00', u'早上08:00-12:00'),
        (u'下午14:00-17:00', u'下午14:00-17:00'),
        (u'晚上19:00-22:30', u'晚上19:00-22:30'),
    )

    organization = models.ForeignKey(Organization)
    date = models.DateField()
    time = MultiSelectField(max_length=100, choices=TIME)
    activity = models.CharField(max_length=30)
    approved = models.BooleanField(default=False)
    application_time = models.DateTimeField(auto_now_add=True)

    plan_file = models.FileField(upload_to=file_save_path('south_stadium'),
                                 validators=[validate_file_extension])
    applicant_name = models.CharField(max_length=10)
    applicant_phone_number = models.CharField(max_length=30)
    activity_summary = models.CharField(max_length=200)
    sponsor = models.CharField(max_length=30, blank=True, null=True)
    sponsorship = models.CharField(max_length=30, blank=True, null=True)
    sponsorship_usage = models.CharField(max_length=40, blank=True, null=True)
    remarks = models.CharField(max_length=300, blank=True, null=True)
    deleted = models.BooleanField(default=False)

    @classmethod
    def generate_table(cls, offset=0):
        ''' generate table
        - date [ 7 * date ]
        - content - ('早上08:00-12:00', [ 7 * [] ] )
                  - ('下午14:00-17:00', [ 7 * [] ] )
                  - ('晚上19:00-22:30', [ 7 * [] ] )
        '''
        apps_whose_field_used_within_7days \
            = get_applications_a_week(cls, offset)
        content = { time: [ [] for i in range(0, 7)] \
                    for time, t in cls.TIME }
        first_day = date.today() + timedelta(offset*7)
        for app in apps_whose_field_used_within_7days:
            for t in app.time:
                content[t][(app.date-first_day).days].append(app)

        return {'date': gennerate_date_list_7days(offset),
                'content': ( (time, content[time]) for time, t in cls.TIME)}

@receiver(post_delete, sender=SouthStadiumApplication)
def Plan_file_delete(sender, instance, **kwargs):
    if instance.plan_file:
        instance.plan_file.delete(False)
