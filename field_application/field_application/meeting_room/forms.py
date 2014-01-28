#-*- coding: utf-8 -*-
from datetime import timedelta

from django import forms
from django.utils import timezone
from django.forms.extras.widgets import SelectDateWidget
from django.forms import Textarea, RadioSelect
from django.forms import CheckboxSelectMultiple 

from field_application.meeting_room.models import MeetingRoomApplication 


class MeetingRoomApplicationForm(forms.ModelForm):
    place = forms.ChoiceField(choices=MeetingRoomApplication.PLACE,
                              widget=RadioSelect())
    class Meta:
        model = MeetingRoomApplication
        exclude = ['organization', 'approved', 'application_time']
        widgets = {
            'date': SelectDateWidget(),
            'meeting_summary': Textarea(),
            'remarks': Textarea(),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        now = timezone.now().date()
        if date < now:
            raise forms.ValidationError('所填日期已过')
        if date > now + timedelta(days=14):
            raise forms.ValidationError('申请的场地使用时间距离现在不能超过14天')
        return date

    def clean(self):
        super(MeetingRoomApplicationForm, self).clean()
        if MeetingRoomApplication.objects.filter(
                place=self.cleaned_data.get('place'),
                date=self.cleaned_data.get('date'),
                time=self.cleaned_data.get('time'),
                approved=True).exists():
            msg = '该时间段已有人申请'
            self._errors['time'] = self.error_class([msg])
            del self.cleaned_data['time']
        return self.cleaned_data

