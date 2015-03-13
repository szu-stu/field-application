#-*- coding: utf-8 -*-
import copy
from datetime import datetime, timedelta, date

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from field_application.account.models import Organization
from field_application.custom.utils import gennerate_date_list_7days 
from field_application.custom.utils import get_applications_a_week 
from field_application.utils.models import file_save_path
from field_application.custom.validators import validate_file_extension
from field_application.custom.model_field import MultiSelectField


class StudentActivityCenterApplication(models.Model):

    PLACE = (
        (u'学生活动中心前广场', u'学生活动中心前广场'),
        # (u'一楼影视报告厅', u'一楼影视报告厅'),
        (u'学生活动中心三楼天台(东)', u'学生活动中心三楼天台(东)'),
        (u'学生活动中心三楼天台(西)', u'学生活动中心三楼天台(西)'),
        (u'石头坞广场', u'石头坞广场'),
    )
    TIME = (
        (u'早上', u'早上'),
        (u'下午', u'下午'),
        (u'晚上', u'晚上'),
    )

    organization = models.ForeignKey(Organization)
    place = models.CharField(max_length=200, choices=PLACE)
    date = models.DateField()
    time = MultiSelectField(max_length=50, choices=TIME)
    activity = models.CharField(max_length=30)
    approved = models.BooleanField(default=False)
    application_time = models.DateTimeField(auto_now_add=True)
    plan_file = models.FileField(
            upload_to=file_save_path('student_activity_center'),
            validators=[validate_file_extension])

    applicant_name = models.CharField(max_length=10)
    applicant_phone_number = models.CharField(max_length=30)
    applicant_stu_id = models.CharField(max_length=15)
    applicant_college = models.CharField(max_length=50)
    activity_summary = models.CharField(max_length=200)
    sponsor = models.CharField(max_length=30, blank=True, null=True)
    sponsorship = models.CharField(max_length=30, blank=True, null=True)
    sponsorship_usage = models.CharField(max_length=40, blank=True, null=True)
    deleted = models.BooleanField(default=False)

    @classmethod
    def generate_table(cls, offset=0):
        ''' generate dict
        -date : [ 7 * date ] 
        -content: 
          学生活动中心前广场      : [7 * [ [], [],[] ] ]
          一楼影视报告厅          : 同上 
          学生活动中心三楼天台(东): 同上 
          学生活动中心三楼天台(西): 同上 
          石头坞广场              : 同上 
        '''
        field_used_this_week_applications = \
                get_applications_a_week(cls, offset)

        empty_time_dict = { time: [] for time, l in cls.TIME }
        content = {place: [ copy.deepcopy(empty_time_dict) for i in range(7)] \
                                for place, p in cls.PLACE }
        first_day = date.today() + timedelta(days=offset*7)
        for app in field_used_this_week_applications:
            for time in app.time:
                content[app.place][(app.date-first_day).days][time].append(app)
        # sort in the order of time
        for place in content:
            for day in range(7):
                content[place][day] = [content[place][day][time] \
                                            for time, t in cls.TIME]
        # sort in the order of place
        content = [(place, content[place]) for place, p in cls.PLACE]
        return {'date': gennerate_date_list_7days(offset),
                'content': content}

@receiver(post_delete, sender=StudentActivityCenterApplication)
def Plan_file_delete(sender, instance, **kwargs):
    if instance.plan_file:
        instance.plan_file.delete(False)
