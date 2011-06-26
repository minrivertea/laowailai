from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from laowailai.list import views


urlpatterns = patterns('',

    url(r'^$', views.news_feed, name="news_feed"),
    url(r'^people/$', views.people, name="people"),
    url(r'^posts/(\w+)/$', views.a_post, name="a_post"),
    url(r'^posts/add$', views.post, name="post"),
    url(r'^set-city/$', views.set_city, name="set_city"),
    url(r'^suggestions/vote/(\w+)$', views.suggestion_vote, name="suggestion_vote"),
    url(r'^suggestions/$', views.suggestions, name="suggestions"),
    url(r'^subscribe/$', views.subscribe, name="subscribe"),
    url(r'^unsubscribe-successful/$', views.unsubscribe_successful, name="unsubscribe_successful"),
    url(r'^unsubscribe/$', views.unsubscribe, name="unsubscribe"),
    url(r'^user-subscribe/$', views.user_subscribe, name="user_subscribe"),
    url(r'^user-unsubscribe/$', views.user_unsubscribe, name="user_unsubscribe"),
    url(r'^newsletter/$', views.newsletter, name="newsletter"),
    url(r'^newsletter_send/$', views.newsletter_send, name="newsletter_send"),
)

