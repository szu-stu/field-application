from django.conf.urls import url, patterns

from field_application.student_activity_center.views import ApplyView
from field_application.student_activity_center.views import display_table
from field_application.student_activity_center.views import display_listing 
from field_application.student_activity_center.views import manage
from field_application.student_activity_center.views import get_detail
from field_application.student_activity_center.views import ModifyView

urlpatterns = patterns(
    '',
    url(r'^apply/$', ApplyView.as_view(), name='apply'),
    url(r'^table/$', display_table, name='table'),
    url(r'^list/$', display_listing, name='listing'),
    url(r'^get_detail/$', get_detail, name='get_detail'),
    url(r'^manage/$', manage, name='manage'),
    url(r'^modify/$', ModifyView.as_view(), name='modify'),
 )
