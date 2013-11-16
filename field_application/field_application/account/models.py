#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):

    user = models.OneToOneField(User)
    org_in_charge = models.CharField(max_length=30)
    tutor = models.CharField(max_length=20)
    tutor_contact_infor = models.CharField(max_length=30)
    director = models.CharField(max_length=20)
    director_contact_infor = models.CharField(max_length=30)
    belong_to = models.CharField(max_length=10)

class OrgActivityLog(models.Model):
    pass
