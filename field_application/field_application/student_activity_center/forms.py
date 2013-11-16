#-*- coding: utf-8 -*-
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from field_application.student_activity_center.models \
        import StudentActivityCenterApplication


class StudentActivityCenterApplicationForm(forms.Form):
    class Meta:
        model = StudentActivityCenterApplication
        exclude = ['organization', 'approved', 'application_time']
        widgets = {
            'date': SelectDateWidget(),
            'activity_summary': Textarea(),
        }
