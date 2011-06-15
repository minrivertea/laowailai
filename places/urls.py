from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from laowailai.places import views


urlpatterns = patterns('',
    url(r'^$', views.places, name="places"),
    url(r'^add/$', views.add_place, name="add_place"),
    url(r'^(\w+)/edit-location/$', views.edit_location, name="edit_location"),
    url(r'^(\w+)/$', views.place, name="place"),
    url(r'^(\w+)/(\w+)/$', views.add_rating, name="add_rating"),
    url(r'^(?P<city>[\w-]+)/(?P<slug>[\w-]+)/$', views.get_place_by_slug, name="get_place_by_slug"),
)

