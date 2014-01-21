from django.conf.urls import url, patterns

from field_application.campus_field.views import ApplyExhibitView
from field_application.campus_field.views import ApplyPublicityView 
from field_application.campus_field.views import display_exhibit_table
from field_application.campus_field.views import display_exhibit_list
from field_application.campus_field.views import display_publicity_table 
from field_application.campus_field.views import display_publicity_list 

urlpatterns = patterns(
    '',
    url(r'^exhibit/apply/$', ApplyExhibitView.as_view(),
        name='apply_exhibit'),
    url(r'^exhibit/table/$', display_exhibit_table,
        name='exhibit_table'),
    url(r'^exhibit/list/$', display_exhibit_list,
        name='exhibit_list'),

    url(r'^publicity/apply/$', ApplyPublicityView.as_view(),
        name='apply_publicity'),
    url(r'^publicity/table/$', display_publicity_table,
        name='publicity_table'),
    url(r'^publicity/list/$', display_publicity_list,
        name='publicity_list'),
 )
