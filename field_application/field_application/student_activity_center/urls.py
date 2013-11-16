from django.conf.urls import url, patterns

from field_application.student_activity_center.views import ApplyView

urlpatterns = patterns(
    '',
    url(r'^apply/$', ApplyView.as_view(), name='apply'),
 )
