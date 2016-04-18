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


# not necessary now
def check_exhibit_board_num(place_list, start_date, end_date,
        time_list, exhibit_board_number):

    board_num_upper_limit = \
            {u'CD座文化长廊': 40, u'A座文化大厅': 30,
             u'西南餐厅前空地': 45, u'荔山餐厅前空地': 45}
    for place in place_list:
        for i in range((end_date-start_date).days+1):
            date = start_date + timedelta(days=i)
            for time in time_list:
                apps = ExhibitApplication.objects.filter(
                        Q(start_date__lte=date) & \
                        Q(end_date__gte=date),
                        place__contains=place,
                        time__contains=time).filter(approved=True)
                used_num = \
                        sum((app.exhibit_board_number for app in apps))
                if used_num + exhibit_board_number > \
                        board_num_upper_limit[place]:
                    msg = place + \
                          date.strftime(' %Y-%m-%d ') + \
                          time + \
                          u'只剩下%d个展板' % \
                        (board_num_upper_limit[place]-used_num)
                    return msg
    return None


class ExhibitApplicationForm(forms.ModelForm):
    exhibit_board_number = forms.IntegerField(min_value=0, max_value=50)
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
        if 'place' not in self.cleaned_data or \
                'exhibit_board_number' not in self.cleaned_data or\
                'start_date' not in self.cleaned_data or \
                'end_date' not in self.cleaned_data or \
                'time' not in self.cleaned_data:
            return super(ExhibitApplicationForm, self).clean()

        # check date
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        if end_date < start_date:
            msg = u'结束时间不能早于开始时间'
            self._errors['end_date'] = self.error_class([msg])
            del self.cleaned_data['end_date']
            return super(ExhibitApplicationForm, self).clean()
        if end_date > start_date + timedelta(days=6):
            msg = u'展览时间不得超过7天'
            self._errors['end_date'] = self.error_class([msg])
            del self.cleaned_data['end_date']
            return super(ExhibitApplicationForm, self).clean()

        return super(ExhibitApplicationForm, self).clean()

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        now = timezone.now().date()
        if start_date < now:
            raise forms.ValidationError(u'所填日期已过')
        if start_date >= now + timedelta(days=14):
            raise forms.ValidationError(
                    u'申请的场地使用时间距离现在不能超过14天')
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        now = timezone.now().date()
        if end_date < now:
            raise forms.ValidationError(u'所填日期已过')
        if end_date >= now + timedelta(days=14):
            raise forms.ValidationError(u'申请的场地使用时间距离现在不能超过14天')
        return end_date

    


#  检查场地是否已经存在通过的申请 not used now
def check_publicity(place_list,
        start_date, end_date, time_list):
    for place in place_list:
        for i in range((end_date-start_date).days+1):
            date = start_date + timedelta(days=i)
            for time in time_list:
                if PublicityApplication.objects.filter(
                        Q(start_date__lte=date) & \
                        Q(end_date__gte=date),
                        place__contains=place,
                        time__contains=time).filter(approved=True):
                    msg = place + \
                          date.strftime(' %Y-%m-%d ') + \
                          time + \
                          u'已经被人使用'
                    return msg
    return None


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
        if start_date >= now + timedelta(days=14):
            raise forms.ValidationError(u'申请的场地使用时间距离现在不能超过14天')
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        now = timezone.now().date()
        if end_date < now:
            raise forms.ValidationError(u'所填日期已过')
        if end_date >= now + timedelta(days=14):
            raise forms.ValidationError(u'申请的场地使用时间距离现在不能超过14天')
        return end_date

    def clean(self):
        if 'place' not in self.cleaned_data or \
                'start_date' not in self.cleaned_data or \
                'end_date' not in self.cleaned_data or \
                'time' not in self.cleaned_data:
            return super(PublicityApplicationForm, self).clean()
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        #  检查开始日期和结束日期 
        if start_date and end_date and end_date < start_date:
            msg = u'结束时间不能早于开始时间'
            self._errors['end_date'] = self.error_class([msg])
            del self.cleaned_data['end_date']
            return super(PublicityApplicationForm, self).clean()
        if start_date and end_date \
                and end_date > start_date + timedelta(days=1):
            msg = u'展览时间不得超过2天'
            self._errors['end_date'] = self.error_class([msg])
            del self.cleaned_data['end_date']

        place = self.cleaned_data.get('place')
        other_place = self.cleaned_data.get('other_place')
        if u'其它' in place and not other_place:
            msg = u"选择‘其它’场地时请在右栏输入框填入所申请的场地"
            self._errors['place'] = self.error_class([msg])
        elif not u'其它' in place and other_place:
            msg = u"若要申请其它场地,请勾选‘其它’,否则右边输入框请留空"
            self._errors['place'] = self.error_class([msg])

        return super(PublicityApplicationForm, self).clean()

