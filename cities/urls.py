from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from laowailai.cities import views
from laowailai.list.views import people


urlpatterns = patterns('',
    (r'^', include('laowailai.list.urls')),
    url(r'^photos/$', views.photos, name="photos"),
    url(r'^add-blog/$', views.add_blog, name="add_blog"),
    (r'^places/', include('laowailai.places.urls')),
    url(r'^people/$', people, name="people"),
    (r'^events/', include('laowailai.events.urls')),
    (r'^questions/', include('laowailai.questions.urls')),
)

