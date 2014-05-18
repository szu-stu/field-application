from django.conf.urls import url, patterns

from field_application.meeting_room.views import display_table
from field_application.meeting_room.views import ListAppView 
from field_application.meeting_room.views import ApplyMeetingRoomView
from field_application.meeting_room.views import get_detail, delete
from field_application.meeting_room.views import ModifyView
from field_application.meeting_room.views import ManageView 
from field_application.meeting_room.views import manager_approve 
from field_application.meeting_room.views import conflict_for_form

urlpatterns = patterns(
    '',
    url(r'^apply/$', ApplyMeetingRoomView.as_view(), name='apply'),
    url(r'^table/$', display_table, name='table'),
    url(r'^list/$', ListAppView.as_view(), name='list'),
    url(r'^manage/$', ManageView.as_view(), name='manage'),
    url(r'^get_detail/$', get_detail, name='get_detail'),
    url(r'^modify/$', ModifyView.as_view(), name='modify'),
    url(r'^delete/$', delete, name='delete'),
    url(r'^manager_approve/$', manager_approve, name='manager_approve'),

    url(r'^conflict_for_form/$', conflict_for_form,
        name='conflict_for_form'),
 )
