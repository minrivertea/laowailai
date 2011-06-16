from django.conf.urls.defaults import *
from django.conf import settings
import django.views.static

from list.feeds import LatestEntriesFeed
from list.views import index, ajax_comment, tell_a_friend, laowai, upload_profile_photo, add_a_bio, like
from cities.views import cities, mark_city

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
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

urlpatterns += patterns('',
    url(r'^/?$', index, name="home_page"),
    url(r'^comments/posted/$', ajax_comment, name="ajax_comment"),
    (r'^comments/', include('django.contrib.comments.urls')), 
    url(r'^cities/$', cities, name="cities"),
    url(r'^mark_city/(\w+)/$', mark_city, name="mark_city"),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^upload_profile_photo/$', upload_profile_photo, name="upload_profile_photo"),
    url(r'^laowai/bio$', add_a_bio, name="add_a_bio"),
    url(r'^laowai/(\w+)/$', laowai, name="laowai"),
    url(r'^like/(\w+)$', like, name="like"),
    (r'^latest/feed/$', LatestEntriesFeed()),
    url(r'^tell-a-friend/$', tell_a_friend, name="tell_a_friend"),
    url(r'^(?P<slug>[\w-]+)/', include('laowailai.cities.urls')),
)
