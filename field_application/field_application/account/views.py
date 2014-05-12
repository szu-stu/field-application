#-*- coding: utf-8 -*-
import logging

from django.views.generic import View
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView, ListView

from field_application.account.permission import guest_or_redirect
from field_application.account.permission import check_perms 
from field_application.account.forms import SignUpForm, SignInForm
from field_application.account.models import UserActivityLog, get_client_ip
from field_application.account.models import Organization
from field_application.account.forms import EditForm


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
            return HttpResponseRedirect(reverse('account:signin'))

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
        UserActivityLog.objects.create(user=request.user,
                                       ip_address=get_client_ip(request),
                                       behavior=u"修改密码")
        return HttpResponseRedirect(reverse('home'))


class EditProfile(UpdateView):
    model = Organization
    form_class = EditForm
    template_name = 'account/edit-profile.html'
    success_url = '/'


class Profile(DetailView):
    model = Organization
    fields = ['chinese_name', 'org_in_charge',
              'tutor','tutor_contact_infor',
              'director', 'director_contact_infor',
              'belong_to', 'is_banned']
    template_name = 'account/profile.html'
    context_object_name = 'organization'


def org_manage(request):
    orgs = Organization.objects.filter(
        user__is_active=True).order_by('-pk')
    return render(request, 'account/org-manage.html',
            {'list': orgs})


@permission_required('account.manager')
def disable_org(request):
    org_id = request.GET.get('id')
    org = get_object_or_404(Organization, id=org_id)
    org.is_banned = not org.is_banned
    org.save()
    return HttpResponseRedirect(reverse('account:org_manage'))


@check_perms('account.manager', message='无管理权限')
def manager_reset_password(request):
    org_id = request.GET.get('id')
    org = get_object_or_404(Organization, id=org_id)
    org.user.set_password('123456')
    org.user.save()
    return HttpResponseRedirect(reverse('account:org_manage'))
