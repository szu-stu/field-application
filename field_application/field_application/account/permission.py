#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render 


def guest_or_redirect(function=None):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated(),
        login_url='/',
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def check_user_pk(function=None):
    def wrapped_check(request, *args, **kwargs):
        if not kwargs.get('pk'):
            raise Exception('url in urls.py need "(?P<pk>\d+)"')
        if request.user.pk != int(kwargs.get('pk')):
            return HttpResponseRedirect(reverse('deny'))
        kwargs['pk'] = request.user.organization.pk
        return function(request, *args, **kwargs)
    return login_required(wrapped_check)


def check_perms(perm, message=u'权限不足'):
    ''' accustomed version of permission_required '''
    def decorator(function):
        def wrapped_check(request, *args, **kwargs):
            if not isinstance(perm, (list, tuple)):
                perms = (perm, )
            else:
                perms = perm
            if not request.user.has_perms(perms):
                return render(request, 'deny.html', {'message': message})
            return function(request, *args, **kwargs)
        return wrapped_check
    return decorator
