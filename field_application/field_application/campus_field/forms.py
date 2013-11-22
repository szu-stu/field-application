#-*- coding: utf-8 -*-
from datetime import timedelta

from django import forms
from django.utils import timezone
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from django.forms import Textarea, RadioSelect
from django.forms import CheckboxSelectMultiple 

from field_application.campus_field.models import ExhibitApplication
from field_application.campus_field.models import PublicityApplication


class ExhibitApplicationForm(forms.ModelForm):
    exhibition = forms.MultipleChoiceField(
            choices=ExhibitApplication.EXHIBITION,
            widget=CheckboxSelectMultiple)
    class Meta:
       model = ExhibitApplication
       exclude = ['organization', 'approved', 'application_time']
       widgets = {
           'start_date': SelectDateWidget(),
           'end_date': SelectDateWidget(),
           'activity_summary': Textarea(),
           'remarks': Textarea(),
           'exhibition': RadioSelect(),
       }

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        now = timezone.now().date()
        if start_date < now:
            raise forms.ValidationError(u'所填日期已过')
        if start_date > now + timedelta(days=14):
            raise forms.ValidationError(u'申请的场地使用时间距离现在不能超过14天')
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        now = timezone.now().date()
        if end_date < now:
            raise forms.ValidationError(u'所填日期已过')
        if end_date > now + timedelta(days=14):
            raise forms.ValidationError(u'申请的场地使用时间距离现在不能超过14天')
        start_date = self.cleaned_data.get('start_date')
        if end_date > start_date + timedelta(days=7):
            raise forms.ValidationError(u'展览时间不得超过7天')
        return end_date


class PublicityApplicationForm(forms.ModelForm):
    class Meta:
       model = PublicityApplication
       exclude = ['organization', 'approved', 'application_time']
       widgets = {
           'start_date': SelectDateWidget(),
           'end_date': SelectDateWidget(),
           'activity_summary': Textarea(),
           'remarks': Textarea(),
       }

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        now = timezone.now().date()
        if start_date < now:
            raise forms.ValidationError(u'所填日期已过')
        if start_date > now + timedelta(days=14):
            raise forms.ValidationError(u'申请的场地使用时间距离现在不能超过14天')
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        now = timezone.now().date()
        if end_date < now:
            raise forms.ValidationError(u'所填日期已过')
        if end_date > now + timedelta(days=14):
            raise forms.ValidationError(u'申请的场地使用时间距离现在不能超过14天')
        start_date = self.cleaned_data.get('start_date')
        if end_date > start_date + timedelta(days=3):
            raise forms.ValidationError(u'展览时间不得超过3天')
        return end_date
