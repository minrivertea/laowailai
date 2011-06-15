from django.conf.urls.defaults import *
from django.conf import settings
import django.views.static

from list.feeds import LatestEntriesFeed
from list.views import index, people, ajax_comment

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/?$', index, name="home_page"),
    url(r'^people/?$', people, name="people"),
    url(r'^comments/posted/$', ajax_comment, name="ajax_comment"),
    (r'^comments/', include('django.contrib.comments.urls')), 
    (r'^feed/', include('fuzhounet.list.urls')),
    (r'^cities/', include('fuzhounet.cities.urls')),
    (r'^events/', include('fuzhounet.events.urls')),
    (r'^places/', include('fuzhounet.places.urls')),
    (r'^questions/', include('fuzhounet.questions.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^latest/feed/$', LatestEntriesFeed()),
)


urlpatterns += patterns('',

    # CSS, Javascript and IMages
    (r'^photos/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT + '/photos',
        'show_indexes': settings.DEBUG}),
    (r'^images/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT + '/images',
        'show_indexes': settings.DEBUG}),
    (r'^thumbs/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT + '/thumbs',
        'show_indexes': settings.DEBUG}),
    (r'^css/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT + '/css',
        'show_indexes': settings.DEBUG}),
    (r'^js/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT + '/js',
        'show_indexes': settings.DEBUG}),
)
