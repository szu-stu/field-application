#-*- coding: utf-8 -*-
from datetime import timedelta, datetime

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms import Textarea, RadioSelect
from django.forms import CheckboxSelectMultiple 

from field_application.integrated_service.models import InteServiceApplication 


class InteServiceApplicationForm(forms.ModelForm):
    place = forms.ChoiceField(choices=InteServiceApplication.PLACE,
                              widget=RadioSelect())
    class Meta:
        model = InteServiceApplication
        exclude = ['organization', 'approved', 'application_time']
        widgets = {
            'date': SelectDateWidget(),
            'summary': Textarea(),
            'remarks': Textarea(),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        now = datetime.now().date()
        if date < now:
            raise forms.ValidationError(u'所填日期已过')
        if date >= now + timedelta(days=14):
            raise forms.ValidationError(
                    u'申请的场地使用时间距离现在不能超过14天')
        return date

    def clean(self):
        if 'time' not in self.cleaned_data or \
                'date' not in self.cleaned_data or \
                'place' not in self.cleaned_data:
            return super(InteServiceApplicationForm, self).clean()
        super(InteServiceApplicationForm, self).clean()

        for time in self.cleaned_data['time']:
            if InteServiceApplication.objects.filter(
                    place=self.cleaned_data.get('place'),
                    date=self.cleaned_data.get('date'),
                    time__contains=time,
                    approved=True).exists():
                msg = time + u'已有人申请'
                self._errors['time'] = self.error_class([msg])
                raise forms.ValidationError(
                    u'您的申请与别人有冲突，请检查')
        return self.cleaned_data
