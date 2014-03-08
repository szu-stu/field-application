#-*- coding: utf-8 -*-
from datetime import timedelta

from django import forms
from django.utils import timezone
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from django.forms import Textarea, RadioSelect, HiddenInput
from django.forms import CheckboxSelectMultiple 

from field_application.south_stadium.models import SouthStadiumApplication


class SouthStadiumApplicationForm(forms.ModelForm):
    class Meta:
       model = SouthStadiumApplication
       exclude = ['organization', 'approved', 'application_time']
       widgets = {
           'organization': HiddenInput(),
           'date': SelectDateWidget(),
           'activity_summary': Textarea(),
           'remarks': Textarea(),
       }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        now = timezone.now().date()
        if date < now:
            raise forms.ValidationError(u'所填日期已过')
        if date == now:
            raise forms.ValidationError(
                    u'不能申请当天的场地，需至少提前一天申请')
        if date > now + timedelta(days=14):
            raise forms.ValidationError(u'申请的场地使用时间距离现在不能超过14天')
        return date

    def clean(self):
        if 'time' not in self.cleaned_data or \
           'date' not in self.cleaned_data:
            return super(SouthStadiumApplicationForm, self).clean()
        super(SouthStadiumApplicationForm, self).clean()
        for time in self.cleaned_data.get('time'):
            if SouthStadiumApplication.objects.filter(
                    date=self.cleaned_data.get('date'),
                    time__contains=time,
                    approved=True).exists():
                # strftime does not support unicode
                msg = self.cleaned_data['date'].strftime('%Y-%m-%d ') \
                        + time + u'已有人使用'
                self._errors['date'] = self.error_class([msg])
                del self.cleaned_data['date']
        return self.cleaned_data

