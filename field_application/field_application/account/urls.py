#-*- coding: utf-8 -*-
from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from field_application.account.permission import check_user_pk, check_perms
from field_application.account.views import org_manage, disable_org
from field_application.account.views import manager_reset_password
from field_application.account.views import SignOutView, SignInView 
from field_application.account.views import SignUpView, ResetPasswordView
from field_application.account.views import EditProfile, Profile


urlpatterns = patterns(
    '',
    url(r'^signin/$', SignInView.as_view(), name='signin'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^signout/$', SignOutView.as_view(), name='signout'),
    url(r'^reset_password/$', ResetPasswordView.as_view(), 
        name='reset_password'),
    url(r'^profile/(?P<pk>\d+)/$',
        check_user_pk(Profile.as_view()), name='profile'),
    url(r'^edit_profile/(?P<pk>\d+)/$', 
        check_user_pk(EditProfile.as_view()), name='edit_profile'),

    # only manager can use
    url(r'^org_manage/$',
        check_perms('account.manager', message=u'无管理权限') \
                (org_manage), name='org_manage'),
    url(r'^disable_org/$',
        check_perms('account.manager', message=u'无管理权限') \
            (disable_org), name='disable_org'),
    # this is used by manager to set password to 123456
    url(r'^manager_reset_password/$', manager_reset_password,
        name='manager_reset_password'),
 )
