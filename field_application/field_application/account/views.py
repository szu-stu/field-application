from django.views.generic import View
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from field_application.account.forms import SignUpForm


class SignInView(View):

    def get(self, request):
        return render(request, 'account/sign-in.html',
                      {'form': AuthenticationForm()})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse('account:signin'))
        return render(request, 'account/sign-in.html', {'form': form})


class SignUpView(View):

    def get(self, request):
        return render(request, 'account/sign-up.html',
                      {'form': SignUpForm()})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('account:signin'))

        return render(request, 'account/sign-up.html', {'form': form})

class SignOutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('account:signin'))
