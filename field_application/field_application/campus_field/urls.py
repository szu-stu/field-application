from django.conf.urls import url, patterns

from field_application.campus_field.views import ApplyExhibitView
from field_application.campus_field.views import ApplyPublicityView 
from field_application.campus_field.views import display_table
from field_application.campus_field.views import display_listing 

urlpatterns = patterns(
    '',
    url(r'^apply-exhibit/$', ApplyExhibitView.as_view(), name='apply_exhibit'),
    url(r'^apply-publicity/$', ApplyPublicityView.as_view(), name='apply_publicity'),
    url(r'^table/$', display_table, name='table'),
    url(r'^list/$', display_listing, name='listing'),
 )
