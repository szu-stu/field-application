#-*- coding: utf-8 -*-
from datetime import timedelta

from django import forms
from django.utils import timezone
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from django.forms import Textarea

from field_application.campus_field.models import ExhibitApplication,
                                                  PublicityApplication


class ExhibitApplicationForm(forms.ModelForm):
     class Meta:
        model = ExhibitApplication
        exclude = ['organization', 'approved', 'application_time']
        widgets = {
            'start_date': SelectDateWidget(),
            'end_date': SelectDateWidget(),
            'activity_summary': Textarea(),
        }



class PublicityApplicationForm(forms.ModelForm):
     class Meta:
        model = ExhibitApplication
        exclude = ['organization', 'approved', 'application_time']
        widgets = {
            'start_date': SelectDateWidget(),
            'end_date': SelectDateWidget(),
            'activity_summary': Textarea(),
        }

