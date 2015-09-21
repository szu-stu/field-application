import os

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

from field_application import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html'),
               name='home'),
    url(r'^deny/$', TemplateView.as_view(template_name='deny.html'),
               name='deny'),
    url(r'^account/', include('field_application.account.urls',
                              namespace='account')),
    url(r'^student_activity_center/',
        include('field_application.student_activity_center.urls',
                namespace='student_activity_center')),
    url(r'^meeting_room/', include('field_application.meeting_room.urls',
                                   namespace='meeting_room')),
    url(r'^exhibit/',
        include('field_application.campus_field.exhibit.urls',
                                   namespace='exhibit')),
    url(r'^publicity/',
        include('field_application.campus_field.publicity.urls',
                                   namespace='publicity')),
    url(r'^integrated_service/',
    include('field_application.integrated_service.urls',
                               namespace='integrated_service')),
    url(r'^document/',
        include('field_application.document.urls',
                                   namespace='document')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # not used now
   #url(r'^south_stadium/', include('field_application.south_stadium.urls',
    #                                namespace='south_stadium')),
)

# serve media file when using developing server
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^uploaded-file/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT,}),
        )
