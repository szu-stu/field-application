from django.conf.urls import url, patterns

from field_application.account.views import SignOutView, SignInView 
from field_application.account.views import SignUpView, ResetPasswordView


urlpatterns = patterns(
    '',
    url(r'^signin/$', SignInView.as_view(), name='signin'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^signout/$', SignOutView.as_view(), name='signout'),
    url(r'^reset_password/$', ResetPasswordView.as_view(), 
        name='reset_password'),
 )
