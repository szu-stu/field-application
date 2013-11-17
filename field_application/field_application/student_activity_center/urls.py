from django.conf.urls import url, patterns

from field_application.student_activity_center.views import ApplyView
from field_application.student_activity_center.views import display_table
from field_application.student_activity_center.views import display_listing 

urlpatterns = patterns(
    '',
    url(r'^apply/$', ApplyView.as_view(), name='apply'),
    url(r'^table/$', display_table, name='table'),
    url(r'^list/$', display_listing, name='listing'),
 )
