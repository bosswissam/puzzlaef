from puzzlaef.views import *
from django.conf import settings
from puzzlaef.dajaxice.core import dajaxice_autodiscover
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template

dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'puzzlaef.views.home', name='home'),
    # url(r'^puzzlaef/', include('puzzlaef.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    url(r'^$', start), 
	url(r'^upload/makeMove', make_move),
	url(r'^upload/profile', upload_profile),
    url(r'^upload/theme', upload_theme),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/profile/$', show_profile),  
    (r'^accounts/', include('puzzlaef.registration.backends.default.urls')), 
    (r'^dajaxice/', include('puzzlaef.dajaxice.urls')), #% settings.DAJAXICE_MEDIA_PREFIX, include('puzzlaef.dajaxice.urls')),

)

urlpatterns += staticfiles_urlpatterns()
