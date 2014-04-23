from django.conf.urls import url, patterns
from django.conf import settings
from django.conf.urls.static import static
from views import Upload_File,del_doc

urlpatterns = patterns('',
    url(r'^$',  Upload_File, name='doc_download'),
    url(r'^delete/$', del_doc , name='del_doc'),

)+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
