#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms import HiddenInput

from field_application.account.models import Organization
from field_application.utils.hanzi2pinyin import trans


class SignInForm(AuthenticationForm):
    username = forms.ModelChoiceField(queryset=Organization.objects.all(),
                                      empty_label='请选择组织')

    def clean_username(self):
        org = Organization.objects.get(
                chinese_name=self.cleaned_data['username'])
        return org.user.username

class SignUpForm(UserCreationForm):

    BELONG_TO_CHOICES = (
        ('OT','其它'),
        ('AU','社团联合会'),
        ('SU','校学生会'),
        )

    chinese_name = forms.CharField(max_length=30)
    org_in_charge = forms.CharField(max_length=30)
    tutor = forms.CharField(max_length=20)
    tutor_contact_infor = forms.CharField(max_length=30)
    director = forms.CharField(max_length=20)
    director_contact_infor = forms.CharField(max_length=30)
    belong_to = forms.ChoiceField(choices=BELONG_TO_CHOICES)

    # force model to save
    def save(self):
        new_user = super(SignUpForm, self).save()
        org = Organization.objects.create(
            user=new_user,
            chinese_name = self.cleaned_data['chinese_name'],
            org_in_charge=self.cleaned_data['org_in_charge'],
            tutor=self.cleaned_data['tutor'],
            tutor_contact_infor=self.cleaned_data['tutor_contact_infor'],
            director=self.cleaned_data['director'],
            director_contact_infor=self.cleaned_data['director_contact_infor'],
            belong_to=self.cleaned_data['belong_to'])
        org.save()
        return org
