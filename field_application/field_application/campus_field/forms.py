#-*- coding: utf-8 -*-
from datetime import timedelta

from django import forms
from django.utils import timezone
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from django.forms import Textarea, RadioSelect
from django.forms import CheckboxSelectMultiple 
from django.db.models import Q

from field_application.campus_field.models import ExhibitApplication
from field_application.campus_field.models import PublicityApplication
from field_application.utils.models import get_second_key


class ExhibitApplicationForm(forms.ModelForm):
    class Meta:
       model = ExhibitApplication
       exclude = ['organization', 'approved', 'application_time']
       widgets = {
           'start_date': SelectDateWidget(),
           'end_date': SelectDateWidget(),
           'activity_summary': Textarea(),
           'remarks': Textarea(),
       }

    def clean_exhibit_board_number(self):
        num = self.cleaned_data.get('exhibit_board_number')
        if num <= 0:
            raise forms.ValidationError(u'展板数应为正数')
        return num

    def clean(self):
        # In django validation workflow, if field is not supply
        # clean_field() will not be called
        if  'place' not in self.cleaned_data or \
            'exhibit_board_number' not in self.cleaned_data or\
            'start_date' not in self.cleaned_data or \
            'end_date' not in self.cleaned_data:
            return super(ExhibitApplicationForm, self).clean()

        exhibit_board_number = self.cleaned_data['exhibit_board_number']
        board_num_upper_limit = {u'CD座文化长廊': 40, u'A座文化大厅': 30,
                                 u'西南餐厅前空地': 45, u'荔山餐厅前空地': 45}
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']

        for place in self.cleaned_data['place']:
            for i in range((end_date-start_date).days+1):
                date = start_date + timedelta(days=i)
                apps = ExhibitApplication.objects.filter(
                        Q(start_date__lte=date) & \
                        Q(end_date__gte=date),
                        place__contains=place).filter(approved=True)
                used_num = sum((app.exhibit_board_number for app in apps))
                if used_num + exhibit_board_number > \
                        board_num_upper_limit[place]:
                    msg = get_second_key(place, ExhibitApplication.PLACE) +\
                        u'只剩下%d个展板' % \
                        (board_num_upper_limit[place]-used_num)
                    self._errors['exhibit_board_number'] = \
                            self.error_class([msg])
                    return super(ExhibitApplicationForm, self).clean()
        return super(ExhibitApplicationForm, self).clean()

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        now = timezone.now().date()
        if start_date < now:
            raise forms.ValidationError(u'所填日期已过')
        if start_date > now + timedelta(days=14):
            raise forms.ValidationError(
                    u'申请的场地使用时间距离现在不能超过14天')
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
        return end_date

    def clean(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date and end_date \
                and end_date > start_date + timedelta(days=2):
            msg = u'展览时间不得超过3天'
            self._errors['end_date'] = self.error_class([msg])
            del self.cleaned_data['end_date']
        return super(PublicityApplicationForm, self).clean()

