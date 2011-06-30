from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from laowailai.places import views


urlpatterns = patterns('',
    url(r'^$', views.places, name="places"),
    url(r'^add/$', views.add_place, name="add_place"),
    url(r'^(\w+)/edit-location/$', views.edit_location, name="edit_location"),
    url(r'^(?P<id>[\w-]+)/add_photo/$', views.add_photo, name="add_photo_to_place"),
    url(r'^(?P<id>[\w-]+)/$', views.place, name="place"),
    url(r'^(\w+)/(\w+)/$', views.add_rating, name="add_rating"),
    url(r'^(?P<slug>[\w-]+)/$', views.get_place_by_slug, name="get_place_by_slug"),
)

