from django.conf.urls import url, patterns

from field_application.campus_field.views import ApplyExhibitView 
from field_application.campus_field.views import display_table
from field_application.campus_field.views import display_listing 

urlpatterns = patterns(
    '',
    url(r'^apply/$', ApplyExhibitView.as_view(), name='apply'),
    url(r'^table/$', display_table, name='table'),
    url(r'^list/$', display_listing, name='listing'),
 )
