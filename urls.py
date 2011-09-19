from django.conf.urls.defaults import *
from django.conf import settings
import django.views.static
from django.views.generic.simple import direct_to_template

from list.feeds import LatestEntriesFeed
from list.views import index, ajax_comment, tell_a_friend, laowai, upload_profile_photo, add_a_bio, like, whats_next, profile, profile_notices, notification_mark_as_read, _check_username
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
    (r'^cache/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT + '/cache',
        'show_indexes': settings.DEBUG}),
)

urlpatterns += patterns('',
    url(r'^/?$', index, name="home_page"),
    
    # direct_to_template URLS
    (r'^error_test/$', direct_to_template, {'template': '500.html'}),
    (r'^robots\.txt$', direct_to_template, {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    (r'^humans\.txt$', direct_to_template, {'template': 'humans.txt', 'mimetype': 'text/plain'}),
    
    # weird ones
    url(r'^whats-next/$', whats_next, name="whats_next"),
    url(r'^comments/posted/$', ajax_comment, name="ajax_comment"),
    
    # other apps URLS
    (r'^comments/', include('django.contrib.comments.urls')), 
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^blog/', include('laowailai.blog.urls')),
    (r'^latest/feed/$', LatestEntriesFeed()),
    url(r'^profile/notices/(\w+)/$', notification_mark_as_read, name="notification_mark_as_read"),
    url(r'^profile/notices/$', profile_notices, name="profile_notices"),
    url(r'^profile/$', profile, name="profile"),
    url(r'^cities/$', cities, name="cities"),
    url(r'^mark_city/(\w+)/$', mark_city, name="mark_city"),
    url(r'^upload_profile_photo/$', upload_profile_photo, name="upload_profile_photo"),
    url(r'^laowai/bio$', add_a_bio, name="add_a_bio"),
    url(r'^laowai/(\w+)/$', laowai, name="laowai"),
    url(r'^like/$', like, name="like"),
    url(r'^like/(\w+)$', like, name="like"),
    url(r'^check_username/$', _check_username, name="check_username"),
    (r'^notifications/', include('notification.urls')),
    url(r'^tell-a-friend/$', tell_a_friend, name="tell_a_friend"),
    
    # the main 'city news feed' URL:
    url(r'^(?P<slug>[\w-]+)/', include('laowailai.cities.urls')),
    
)
