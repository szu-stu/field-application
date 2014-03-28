from django.conf.urls import url, patterns

from field_application.campus_field.exhibit.views import ApplyView
from field_application.campus_field.exhibit.views import display_table 
from field_application.campus_field.exhibit.views import display_list 
from field_application.campus_field.exhibit.views import ModifyView 
from field_application.campus_field.exhibit.views import manage, delete
from field_application.campus_field.exhibit.views import get_detail
from field_application.campus_field.exhibit.views import manager_approve 


urlpatterns = patterns(
    '',
    url(r'^apply/$', ApplyView.as_view(), name='apply'),
    url(r'^table/$', display_table, name='table'),
    url(r'^list/$', display_list, name='list'),
    url(r'^manage/$', manage, name='manage'),
    url(r'^get_detail/$', get_detail, name='get_detail'),
    url(r'^modify/$', ModifyView.as_view(), name='modify'),
    url(r'^delete/$', delete, name='delete'),
    url(r'^manager_approve/$', manager_approve, name='manager_approve'),
)
