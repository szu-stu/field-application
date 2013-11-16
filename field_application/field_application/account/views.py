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


class SignInView(View):

    @method_decorator(guest_or_redirect)
    def get(self, request):
        return render(request, 'account/sign-in.html',
                      {'form': SignInForm()})

    @method_decorator(guest_or_redirect)
    def post(self, request):
        form = SignInForm(data=request.POST)
        if not form.is_valid():
            return render(request, 'account/sign-in.html', {'form': form})

        user = form.get_user()
        login(request, user)
        UserActivityLog.objects.create(user=user,
                                       ip_address=get_client_ip(request),
                                       behavior="Login")
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
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('account:signin'))

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
