#-*- coding: utf-8 -*-
import logging

from django.views.generic import View
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm

from field_application.account.permission import guest_or_redirect
from field_application.account.forms import SignUpForm, SignInForm
from field_application.account.models import UserActivityLog, get_client_ip


logger = logging.getLogger(__name__)


class SignInView(View):

    @method_decorator(guest_or_redirect)
    def get(self, request):
        return render(request, 'account/sign-in.html',
                      {'form': SignInForm(),
                       'next': request.GET.get('next')})

    @method_decorator(guest_or_redirect)
    def post(self, request):
        form = SignInForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'account/sign-in.html', {'form': form})

        user = form.get_user()
        if not hasattr(user, 'organization'):
            error_message = '''some one is using a user who don't have
                               corresponding organization(super user
                               for example) to apply. Please check it.'''
            logger.error(error_message)
            form.errors['__all__'] = form.error_class(
                ["user doesn't has corresponding org"]
            )
            return render(request, 'account/sign-in.html', {'form': form})

        login(request, user)
        UserActivityLog.objects.create(user=user,
                                       ip_address=get_client_ip(request),
                                       behavior="Login")
        if request.GET.get('next'):
            return HttpResponseRedirect(request.GET.get('next'))
        else:
            error_message = '''现在的设计是,网站内没有一个可以进入登录界面的
            链接.这个错误信息出现,说明有人直接通过url进入到登录页面,或者有人
            在网站内增加了通向登录界面的链接.
            现在进入登录界面的方式都是靠重定向,这个时候会获取next值,
            也就是在登录成功后需要重定向的url.
            当前,如果next值没有给出,将重定向到首页.
            如果后来新加了可以通向登录界面的链接,请根据你的需求修改这段代码.
            '''
            logger.error(error_message)
            return HttpResponseRedirect(reverse('home'))


class SignUpView(View):

    @method_decorator(guest_or_redirect)
    def get(self, request):
        return render(request, 'account/sign-up.html',
                      {'form': SignUpForm()})

    @method_decorator(guest_or_redirect)
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))

        return render(request, 'account/sign-up.html', {'form': form})


class SignOutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('home'))


class ResetPasswordView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'account/reset-password.html',
                      {'form': PasswordChangeForm(user=request.user)})

    @method_decorator(login_required)
    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if not form.is_valid():
            return render(request, 'account/reset-password.html',
                          {'form': form})
        form.save()
        UserActivityLog.objects.create(user=user,
                                       ip_address=get_client_ip(request),
                                       behavior="change password")
        return HttpResponseRedirect(reverse('home'))
