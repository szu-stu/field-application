from django.conf.urls import url, patterns
from django.conf import settings
from django.conf.urls.static import static
from views import Upload_File,del_doc,index

urlpatterns = patterns('',
    url(r'^$',  index, name='doc_index'),
    url(r'^delete/$', del_doc , name='del_doc'),
    url(r'^modify/$', Upload_File , name='doc_upload'),

)+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
