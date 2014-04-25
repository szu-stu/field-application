from django.conf.urls import url, patterns
from django.conf import settings
from django.conf.urls.static import static
from field_application.document.views import UploadFileView,delete,index

urlpatterns = patterns('',
    url(r'^$',  index, name='index'),
    url(r'^delete/$', delete, name='delete'),
    url(r'^modify/$', UploadFileView.as_view(), name='upload'),

)
