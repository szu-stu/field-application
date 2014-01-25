from django.conf.urls import url, patterns

from field_application.south_stadium.views import ApplyView
from field_application.south_stadium.views import display_table
from field_application.south_stadium.views import display_listing
from field_application.south_stadium.views import message 
from field_application.south_stadium.views import manage, ModifyView

urlpatterns = patterns(
    '',
    url(r'^apply/$', ApplyView.as_view(), name='apply'),
    url(r'^table/$', display_table, name='table'),
    url(r'^list/$', display_listing, name='listing'),
    url(r'^message/$', message, name='message'),
    url(r'^manage/$', manage, name='manage'),
    url(r'^modify/$', ModifyView.as_view(), name='modify'),
 )
