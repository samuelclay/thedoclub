from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'homepage.views.home', name='home'),
    url(r'^presentation/create/?', 'presentation.views.create', name='presentation-create'),
    url(r'^presentation/(?P<presentation_uuid>\w+)/edit/?', 'presentation.views.edit', name='presentation-edit'),
    url(r'^presentation/(?P<presentation_uuid>\w+)/?', 'presentation.views.view', name='presentation-view'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()