#-*- coding: utf-8 -*-
from datetime import timedelta

from django import forms
from django.utils import timezone
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from django.forms import Textarea, RadioSelect
from django.forms import CheckboxSelectMultiple 

from field_application.south_stadium.models import SouthStadiumApplication


class SouthStadiumApplicationForm(forms.ModelForm):
    class Meta:
       model = SouthStadiumApplication
       exclude = ['organization', 'approved', 'application_time']
       widgets = {
           'date': SelectDateWidget(),
           'activity_summary': Textarea(),
           'remarks': Textarea(),
       }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        now = timezone.now().date()
        if date < now:
            raise forms.ValidationError(u'所填日期已过')
        if date > now + timedelta(days=14):
            raise forms.ValidationError(u'申请的场地使用时间距离现在不能超过14天')
        return date

    def clean(self):
        super(SouthStadiumApplicationForm, self).clean()
        if SouthStadiumApplication.objects.filter(
                date=self.cleaned_data.get('date'),
                time=self.cleaned_data.get('time'),
                approved=True).exists():
            raise forms.ValidationError(u'该时间段已有人使用')
        return self.cleaned_data

