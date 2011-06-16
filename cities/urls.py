from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from laowailai.cities import views


urlpatterns = patterns('',
    url(r'^$', views.city, name="city"),
    (r'^places/', include('laowailai.places.urls')),
    (r'^feed/', include('laowailai.list.urls')),
    (r'^events/', include('laowailai.events.urls')),
    (r'^questions/', include('laowailai.questions.urls')),
    url(r'^mark_city/(\w+)/$', views.mark_city, name="mark_city"),
)

