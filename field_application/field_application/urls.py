from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^account/', include('field_application.account.urls',
                              namespace='account')),
    # Examples:
    # url(r'^$', 'field_application.views.home', name='home'),
    # url(r'^field_application/', include('field_application.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
