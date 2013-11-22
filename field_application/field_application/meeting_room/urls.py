from django.conf.urls import url, patterns

from field_application.meeting_room.views import display_table, display_listing
from field_application.meeting_room.views import ApplyMeetingRoomView

urlpatterns = patterns(
    '',
    url(r'^apply/$', ApplyMeetingRoomView.as_view(), name='apply'),
    url(r'^table/$', display_table, name='table'),
    url(r'^list/$', display_listing, name='listing'),
 )
