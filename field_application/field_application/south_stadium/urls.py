from django.conf.urls import url, patterns

from field_application.south_stadium.views import ApplyView
from field_application.south_stadium.views import display_table
from field_application.south_stadium.views import display_listing
from field_application.south_stadium.views import display_message

urlpatterns = patterns(
    '',
    url(r'^apply/$', ApplyView.as_view(), name='apply'),
    url(r'^table/$', display_table, name='table'),
    url(r'^list/$', display_listing, name='listing'),
    url(r'^message/$', display_listing, name='message'),
 )
