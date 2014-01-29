from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

from field_application.account.permission import check_user_pk 
from field_application.account.views import SignOutView, SignInView 
from field_application.account.views import SignUpView, ResetPasswordView
from field_application.account.views import EditProfile, Profile
from field_application.account.views import Org_manage, disable_org


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
    url(r'^org_manage/$', Org_manage.as_view(), name='org_manage'),
    url(r'^disable_org/$', disable_org, name='disable_org'),
 )
