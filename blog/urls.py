from django.conf.urls.defaults import *
from blog import views


urlpatterns = patterns('',
    url(r'^$', views.index, name="blog_home"),
    url(r'^more/$', views.more, name="more"),
    url(r'^even-more/$', views.even_more, name="even_more"),
    url(r'^(?P<slug>[\w-]+)/$', views.blog_entry, name="blog_entry"),
)
