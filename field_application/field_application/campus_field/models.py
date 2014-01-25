#-*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta

from django.utils import timezone
from django.db import models
from django.db.models import Q

from field_application.account.models import Organization
from field_application.custom.model_field import MultiSelectField
from field_application.custom.utils import gennerate_date_list_7days 
from field_application.custom.utils import get_application_this_week
from field_application.utils.models import file_save_path
from field_application.utils.models import get_first_key


class CampusFieldApplication(models.Model):

    organization = models.ForeignKey(Organization)
    start_date = models.DateField()
    end_date = models.DateField()
    activity = models.CharField(max_length=30)
    approved = models.BooleanField(default=False)
    application_time = models.DateTimeField(auto_now_add=True)

    plan_file = models.FileField(upload_to=file_save_path('campus_field'))
    applicant_name = models.CharField(max_length=10)
    applicant_phone_number = models.CharField(max_length=30)
    activity_summary = models.CharField(max_length=200)
    sponsor = models.CharField(max_length=30, blank=True, null=True)
    sponsorship = models.CharField(max_length=30, blank=True, null=True)
    sponsorship_usage = models.CharField(max_length=40, blank=True, null=True)
    remarks = models.CharField(max_length=300, blank=True, null=True)

    @classmethod
    def get_applications_a_week(cls, offset=0):
        ''' most are the same as custom.utils.get_application_a_week
            except the filter logic '''
        now = timezone.now().date()
        first_day = now + timedelta(days=7*offset)
        last_day = first_day + timedelta(days=6)
        applications_in_the_next_7days = cls.objects.filter(
            Q(start_date__lte=last_day) & Q(end_date__gte=first_day))
        return applications_in_the_next_7days 


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
        ('PIC', u'图片'),
        ('POS', u'海报'),
    )

    place = MultiSelectField(max_length=200, choices=PLACE)
    time = MultiSelectField(max_length=10, choices=TIME)
    exhibition = models.CharField(max_length=20, choices=EXHIBITION)
    other_exhibition = models.CharField(max_length=20,
                                        blank=True, null=True)
    exhibit_board_number = models.PositiveIntegerField()

    @classmethod
    def generate_table(cls, offset=0):
        ''' generate a dict of the structure below
        table - date : [ 7 date ]
              - CD座文化长廊   : [ 7 * {'MOR': [], 'AFT': []} ]
              - A座文化大厅    : [ 7 * {'MOR': [], 'AFT': []} ] 
              - 西南餐厅前空地 : [ 7 * {'MOR': [], 'AFT': []} ] 
              - 荔山餐厅前空地 : [ 7 * {'MOR': [], 'AFT': []} ]
        [] contain all application which contain the same period
        '''
        field_used_this_week_applications = cls.get_applications_a_week(offset)
        first_day = timezone.now().date() + timedelta(days=7*offset)
        last_day = first_day + timedelta(days=6)
        table = {}
        for short_name, full_name in cls.PLACE:
            table[full_name] = [{'MOR': [], 'AFT': []} for i in range(7)]
            apps = field_used_this_week_applications.filter(
                    place__contains=get_first_key(full_name, cls.PLACE))
            for app in apps:
                for i in range((app.end_date-app.start_date).days+1):
                    d = app.start_date + timedelta(days=i)
                    if d < first_day or d > last_day: 
                        continue
                    if 'MOR' in app.time:
                        table[full_name][(d-first_day).days] \
                                ['MOR'].append(app)
                    if 'AFT' in app.time:
                        table[full_name][(d-first_day).days] \
                                ['AFT'].append(app)
        table['date'] = gennerate_date_list_7days(offset)
        return table


class PublicityApplication(CampusFieldApplication):

    PLACE = (
        ('LS', u'荔山餐厅前空地'),
        ('SW', u'西南餐厅前空地'),
        ('WS', u'文山湖路口'),
        ('GM', u'桂庙路口'),
        ('CD', u'CD座文化长廊'),
        ('A', u'A座文化大厅'),
    )
   
    TIME = (
        ('8', '8点-9点'),
        ('9', '9点-10点'),
        ('10', '10点-11点'),
        ('11', '11点-12点'),
        ('12', '12点-13点'),
        ('13', '13点-14点'),
        ('14', '14点-15点'),
        ('15', '15点-16点'),
        ('16', '16点-17点'),
        ('17', '17点-18点'),
        ('18', '18点-19点'),
    )

    ACTIVITY_TYPE = (
        ('LEAFLET', '派传单'),
        ('STAND', '设点'),
    )

    activity_type = models.CharField(max_length=10, choices=ACTIVITY_TYPE)
    other_activity_type = models.CharField(max_length=10,
                                           blank=True, null=True)
    place = MultiSelectField(max_length=200, choices=PLACE)
    time = MultiSelectField(max_length=5, choices=TIME)

    @classmethod
    def generate_table(cls, offset=0):
        ''' generate a dict of the structure below
        table - date : [ 7 date ]
              - CD座文化长廊   : [ 7 * {'8': [], '9': [], ... '19': []} ]
              - A座文化大厅    : [ 7 * {'8': [], '9': [], ... '19': []} ] 
              - 西南餐厅前空地 : [ 7 * {'8': [], '9': [], ... '19': []} ] 
              - 荔山餐厅前空地 : [ 7 * {'8': [], '9': [], ... '19': []} ]
              - 文山湖路口     : [ 7 * {'8': [], '9': [], ... '19': []} ] 
              - 桂庙路口       : [ 7 * {'8': [], '9': [], ... '19': []} ]
        [] contain all application which contain the same period
        [] of '19' is empty, adjust to the empty lattice in the table
        '''
        field_used_this_week_applications = cls.get_applications_a_week(offset)
        first_day = timezone.now().date() + timedelta(days=7*offset)
        last_day = first_day + timedelta(days=6)
        table = {}
        for short_name, full_name in cls.PLACE:
            table[full_name] = [{str(j): [] for j in range(8, 20)} \
                                                for i in range(7)]
            apps = field_used_this_week_applications.filter(
                    place__contains=get_first_key(full_name, cls.PLACE))
            for app in apps:
                for i in range((app.end_date-app.start_date).days+1):
                    d = app.start_date + timedelta(days=i)
                    if d < first_day or d > last_day: 
                        continue
                    for t in app.time:
                        table[full_name][(d-first_day).days][t].append(app)
        table['date'] = gennerate_date_list_7days(offset)
        return table
