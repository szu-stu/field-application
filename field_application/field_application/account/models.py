#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    user = models.OneToOneField(User)
    chinese_name = models.CharField(max_length=30, unique=True)
    org_in_charge = models.CharField(max_length=30)
    tutor = models.CharField(max_length=20)
    tutor_contact_infor = models.CharField(max_length=30)
    director = models.CharField(max_length=20)
    director_contact_infor = models.CharField(max_length=30)
    belong_to = models.CharField(max_length=10)


class UserActivityLog(models.Model):
    user = models.ForeignKey(User)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    behavior = models.CharField(max_length=250)


def get_client_ip(request):
    '''Get the ip of client'''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
