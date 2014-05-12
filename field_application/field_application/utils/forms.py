#-*- coding: utf-8 -*-
from django import forms

class SearchForm(forms.Form):

    SEARCH_CHOICES = (
        ('org', u'申请组织'),
        ('title', u'活动标题'),
        ('place', u'活动地点'),
    )

    APPROVED_CHOICES = (
        ('all', u'全部'),
        ('yes', u'已批准'),
        ('no', u'未批准'),
    )

    search_type = forms.ChoiceField(choices=SEARCH_CHOICES)
    search_value = forms.CharField(max_length=40, required=False)
    approved = forms.ChoiceField(choices=APPROVED_CHOICES)

