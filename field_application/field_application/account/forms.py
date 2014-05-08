#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms import HiddenInput

from field_application.account.models import Organization


BELONG_TO_CHOICES = (
    ('其它','其它'),
    ('社团联合会','社团联合会'),
    ('校学生会','校学生会'),
    )

class SignInForm(AuthenticationForm):

    # 由于这部分django没有翻译，所以直接重写错误信息
    # 注意这不是文档中有说明的接口，当前版本是1.5.1，可能会在新版本失效
    error_messages = {
        'invalid_login': u'请输入正确的组织名和密码',
        'inactive': u'该帐号处于停用状态',
    }

    username = forms.ModelChoiceField(queryset=Organization.objects.all(),
                                      empty_label=u'')

    def clean_username(self):
        ''' change Organization.chinese_name to User.username '''
        org = Organization.objects.get(
                chinese_name=self.cleaned_data['username'])
        if org.is_banned and not org.user.has_perm('account.manager'):
            raise forms.ValidationError(u'该用户已被禁止使用')
        return org.user.username

class SignUpForm(UserCreationForm):

    chinese_name = forms.CharField(max_length=30)
    org_in_charge = forms.CharField(max_length=30)
    tutor = forms.CharField(max_length=20)
    tutor_contact_infor = forms.CharField(max_length=30)
    director = forms.CharField(max_length=20)
    director_contact_infor = forms.CharField(max_length=30)
    belong_to = forms.ChoiceField(choices=BELONG_TO_CHOICES)

    def clean_chinese_name(self):
        chinese_name = self.cleaned_data.get('chinese_name')
        if Organization.objects.filter(chinese_name=chinese_name).exists():
            raise forms.ValidationError(u'该中文名已被注册')
        return chinese_name

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


class EditForm(forms.ModelForm):
    belong_to = forms.ChoiceField(choices=BELONG_TO_CHOICES)
    class Meta:
        model = Organization
        exclude = ('chinese_name', 'user', 'is_banned')

