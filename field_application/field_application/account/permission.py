#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404

from field_application.meeting_room.models import MeetingRoomApplication


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
            return render(request, 'deny.html',
                    {'message': u'url上的id并非你的帐号'})
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


def check_ownership(ApplicationModel):
    ''' Check whether the application is belong to the user 
        or the user is manager
    '''
    def decorator(function):
        def wrapped_check(request, *args, **kwargs):
            app_id = request.GET.get('id')
            if not app_id:
                return render(request, 'deny.html',
                        {'message': u'非法地址'})
            app = get_object_or_404(ApplicationModel, id=app_id)
            if request.user.organization.id != app.organization.id \
                    and not request.user.has_perm('account.manager'):
                return render(request, 'deny.html',
                        {'message': u'不能修改他人申请表'})
            return function(request, *args, **kwargs)
        return wrapped_check
    return decorator


def check_MeetingRoomManager(message=u'权限不足'):
    ''' specialization for meeting room '''
    def decorator(function):
        def wrapped_check(request, *args, **kwargs):
            app_id = request.GET.get('id')
            if not app_id:
                return render(request, 'deny.html',
                        {'message': u'非法地址'})
            app = get_object_or_404(MeetingRoomApplication, id=app_id)
            user = request.user
            if not user.has_perm('account.manager') \
                    and not (app.place == u'石头坞一楼会议室' and \
                        user.has_perm('account.StoneDock1stFloorMeetingRoomManager')) \
                    and not (app.place == u'石头坞二楼会议室' and \
                        user.has_perm('account.StoneDock2ndFloorMeetingRoomManager')):
                return render(request, 'deny.html', {'message': message})
            return function(request, *args, **kwargs)
        return wrapped_check
    return decorator


def check_ownership_MeetingRoom(function):
    ''' specialization for meeting room '''
    def wrapped_check(request, *args, **kwargs):
        app_id = request.GET.get('id')
        if not app_id:
            return render(request, 'deny.html',
                    {'message': u'非法地址'})
        app = get_object_or_404(MeetingRoomApplication, id=app_id)
        user = request.user
        if user.organization.id != app.organization.id \
                and not user.has_perms('account.manager') \
                and not (app.place == u'石头坞一楼会议室' and \
                    user.has_perm('account.StoneDock1stFloorMeetingRoomManager')) \
                and not (app.place == u'石头坞二楼会议室' and \
                    user.has_perm('account.StoneDock2ndFloorMeetingRoomManager')):
            return render(request, 'deny.html',
                    {'message': u'不能修改他人申请表'})
        return function(request, *args, **kwargs)
    return wrapped_check



def check_not_approved(ApplicationModel):
    ''' Check whether the application is already approved'''
    def decorator(function):
        def wrapped_check(request, *args, **kwargs):
            app_id = request.GET.get('id')
            if not app_id:
                return render(request, 'deny.html',
                        {'message': u'非法地址'})
            app = get_object_or_404(ApplicationModel, id=app_id)
            if app.approved:
                return render(request, 'deny.html',
                        {'message': u'不能修改已通过审批的申请表'})
            return function(request, *args, **kwargs)
        return wrapped_check
    return decorator

