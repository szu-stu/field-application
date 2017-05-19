#-*- coding: utf-8 -*-
from datetime import timedelta, datetime

from django import forms
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from django.forms import Textarea

from field_application.student_activity_center.models \
        import StudentActivityCenterApplication


class StudentActivityCenterApplicationForm(ModelForm):
    class Meta:
        model = StudentActivityCenterApplication
        exclude = ['organization', 'approved', 'application_time']
        widgets = {
            'date': SelectDateWidget(),
            'activity_summary': Textarea(),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        d1 = date.replace(2017, 6, 8) #COMMENT AFTER 20170611
        d2 = date.replace(2017, 6, 11) #COMMENT AFTER 20170611
        now = datetime.now().date()
        if date < now:
            raise forms.ValidationError(u'所填日期已过')
        if date >= now + timedelta(days=14):
            raise forms.ValidationError(u'申请的场地使用时间距离现在不能超过14天')
        if (date >= d1) and (date <= d2): #COMMENT AFTER 20170611
            raise forms.ValidationError(u'四创嘉年华 不开放申请') #COMMENT AFTER 20170611
        return date

    def clean(self):
        if 'time' not in self.cleaned_data or \
                'date' not in self.cleaned_data or \
                'place' not in self.cleaned_data:
            return super(StudentActivityCenterApplicationForm, self).clean()
        super(StudentActivityCenterApplicationForm, self).clean()

        for time in self.cleaned_data['time']:
            if StudentActivityCenterApplication.objects.filter(
                    place=self.cleaned_data.get('place'),
                    date=self.cleaned_data.get('date'),
                    time__contains=time,
                    ).exists():
                msg = time + u'已有人申请'
                self._errors['time'] = self.error_class([msg])
                raise forms.ValidationError(
                    u'您的申请与别人有冲突，请检查')
        return self.cleaned_data

