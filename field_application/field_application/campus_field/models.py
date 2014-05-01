#-*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta

from django.db import models
from django.db.models import Q
from django.db.models.signals import post_delete
from django.dispatch import receiver

from field_application.account.models import Organization
from field_application.custom.model_field import MultiSelectField
from field_application.custom.utils import gennerate_date_list_7days 
from field_application.custom.utils import get_application_this_week
from field_application.utils.models import file_save_path
from field_application.utils.models import get_first_key
from field_application.custom.validators import validate_file_extension


class CampusFieldApplication(models.Model):

    organization = models.ForeignKey(Organization)
    start_date = models.DateField()
    end_date = models.DateField()
    activity = models.CharField(max_length=30)
    approved = models.BooleanField(default=False)
    application_time = models.DateTimeField(auto_now_add=True)

    plan_file = models.FileField(upload_to=file_save_path('campus_field'),
                                 validators=[validate_file_extension])
    applicant_name = models.CharField(max_length=10)
    applicant_phone_number = models.CharField(max_length=30)
    applicant_stu_id = models.CharField(max_length=15)
    applicant_college = models.CharField(max_length=50)
    activity_summary = models.CharField(max_length=200)
    sponsor = models.CharField(max_length=30, blank=True, null=True)
    sponsorship = models.CharField(max_length=30, blank=True, null=True)
    sponsorship_usage = models.CharField(max_length=40, blank=True, null=True)
    remarks = models.CharField(max_length=300, blank=True, null=True)
    deleted = models.BooleanField(default=False)

    @classmethod
    def get_applications_a_week(cls, offset=0):
        ''' most are the same as custom.utils.get_application_a_week
            except the filter logic '''
        now = datetime.now().date()
        first_day = now + timedelta(days=7*offset)
        last_day = first_day + timedelta(days=6)
        applications_in_the_next_7days = cls.objects.filter(
            Q(start_date__lte=last_day) & Q(end_date__gte=first_day))
        return applications_in_the_next_7days 

    @classmethod
    def generate_table(cls, offset=0):
        ''' generate a dict of the structure below
        table - date : [ 7 date ]
              - ( place1, [ 7 * [ len(cls.TIME)* [] ] ] )
              - ( place2, 同上
              - ( place3, 同上
        [[], []] 的第一个是早上，二个是下午
        '''
        content = { place: [ {time: [] for time, t in cls.TIME} \
                                for i in range(7)] \
                                for place, p in cls.PLACE }

        field_used_this_week_applications = \
                cls.get_applications_a_week(offset)
        first_day = datetime.now().date() + timedelta(days=7*offset)
        last_day = first_day + timedelta(days=6)
        for app in field_used_this_week_applications:
            for i in range((app.end_date-app.start_date).days+1):
                d = app.start_date + timedelta(days=i)
                if d < first_day or d > last_day: 
                    continue
                for time in app.time:
                    for place in app.place:
                        content[place][(d-first_day).days] \
                                [time].append(app)
        # sort in the order of time
        for place, p in cls.PLACE:
            for i in range(7):
                content[place][i] = [content[place][i][time] \
                                        for time, t in cls.TIME]
                # 特殊处理PublicityApplication的情况，
                # 由于表格要求十二个格子，
                # TIME只有11个，加一个空的补足12
                if len(content[place][i]) == 11:
                    content[place][i].append([])
        # sort in the order of place
        content = [(place, content[place]) for place, p in cls.PLACE]
        return {'date': gennerate_date_list_7days(offset),
                'content': content}


class ExhibitApplication(CampusFieldApplication):

    PLACE = (
        (u'CD座文化长廊', u'CD座文化长廊'),
        (u'A座文化大厅', u'A座文化大厅'),
    )
    
    TIME = (
        (u'早上', u'早上'),
        (u'下午', u'下午'),
    )

    EXHIBITION = (
        (u'图片', u'图片'),
        (u'海报', u'海报'),
    )

    place = MultiSelectField(max_length=200, choices=PLACE)
    time = MultiSelectField(max_length=100, choices=TIME)
    exhibition = models.CharField(max_length=20, choices=EXHIBITION,
                                  blank=True, null=True)
    other_exhibition = models.CharField(max_length=20,
                                        blank=True, null=True)
    exhibit_board_number = models.PositiveIntegerField()


class PublicityApplication(CampusFieldApplication):

    PLACE = (
        (u'荔山餐厅前空地', u'荔山餐厅前空地'),
        (u'西南餐厅前空地', u'西南餐厅前空地'),
        (u'南区天桥', u'南区天桥'),
        (u'南区食堂前空地', u'南区食堂前空地'),
        (u'其它', u'其它'),
    )
   
    TIME = (
        (u'8点-9点', u'8点-9点'),
        (u'9点-10点', u'9点-10点'),
        (u'10点-11点', u'10点-11点'),
        (u'11点-12点', u'11点-12点'),
        (u'12点-13点', u'12点-13点'),
        (u'13点-14点', u'13点-14点'),
        (u'14点-15点', u'14点-15点'),
        (u'15点-16点', u'15点-16点'),
        (u'16点-17点', u'16点-17点'),
        (u'17点-18点', u'17点-18点'),
        (u'18点-19点', u'18点-19点'),
    )

    ACTIVITY_TYPE = (
        (u'派传单', u'派传单'),
        (u'设点', u'设点'),
    )

    activity_type = models.CharField(max_length=10, choices=ACTIVITY_TYPE,
                                     blank=True, null=True)
    other_activity_type = models.CharField(max_length=10,
                                           blank=True, null=True)
    place = MultiSelectField(max_length=200, choices=PLACE)
    other_place = models.CharField(max_length=30, null=True, blank=True)
    time = MultiSelectField(max_length=300, choices=TIME)

@receiver(post_delete, sender=CampusFieldApplication)
def Plan_file_delete(sender, instance, **kwargs):
    if instance.plan_file :
        instance.plan_file.delete(False)


