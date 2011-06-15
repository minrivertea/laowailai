from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from laowailai.cities import views


urlpatterns = patterns('',
    url(r'^$', views.cities, name="cities"),
    url(r'^mark_city/(\w+)/$', views.mark_city, name="mark_city"),
    url(r'^(?P<slug>[\w-]+)/$', views.city, name="city"),
)

