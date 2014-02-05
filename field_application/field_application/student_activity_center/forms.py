#-*- coding: utf-8 -*-
from datetime import timedelta

from django import forms
from django.utils import timezone
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
        now = timezone.now().date()
        if date < now:
            raise forms.ValidationError(u'所填日期已过')
        if date > now + timedelta(days=14):
            raise forms.ValidationError(u'申请的场地使用时间距离现在不能超过14天')
        return date

    def clean(self):
        super(StudentActivityCenterApplicationForm, self).clean()
        if StudentActivityCenterApplication.objects.filter(
                place=self.cleaned_data.get('place'),
                date=self.cleaned_data.get('date'),
                time=self.cleaned_data.get('time'),
                approved=True).exists():
            msg = self.cleaned_data['date'].strftime('%Y-%m-%d ') \
                    + self.cleaned_data['time'] + u'已有人使用'
            self._errors['date'] = self.error_class([msg])
            del self.cleaned_data['date']
        return self.cleaned_data

