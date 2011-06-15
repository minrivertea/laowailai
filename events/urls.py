from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from fuzhounet.events import views


urlpatterns = patterns('',
    url(r'^$', views.events, name="events"),
    url(r'^add/$', views.add_event, name="add_event"),
    url(r'^(\w+)/$', views.event, name="event"),

)

