from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from fuzhounet.list import views


urlpatterns = patterns('',

    url(r'^$', views.news_feed, name="news_feed"),
    url(r'^people/$', views.people, name="people"),
    url(r'^posts/(\w+)/$', views.a_post, name="a_post"),
    url(r'^posts/add$', views.post, name="post"),
    url(r'^suggestions/vote/(\w+)$', views.suggestion_vote, name="suggestion_vote"),
    url(r'^suggestions/$', views.suggestions, name="suggestions"),
    url(r'^subscribe/$', views.subscribe, name="subscribe"),
    url(r'^unsubscribe-successful/$', views.unsubscribe_successful, name="unsubscribe_successful"),
    url(r'^unsubscribe/$', views.unsubscribe, name="unsubscribe"),
    url(r'^like/(\w+)$', views.like, name="like"),
    url(r'^user-subscribe/$', views.user_subscribe, name="user_subscribe"),
    url(r'^user-unsubscribe/$', views.user_unsubscribe, name="user_unsubscribe"),
    url(r'^upload_profile_photo/$', views.upload_profile_photo, name="upload_profile_photo"),
    url(r'^laowai/bio$', views.add_a_bio, name="add_a_bio"),
    url(r'^laowai/(\w+)/$', views.laowai, name="laowai"),
    url(r'^tell-a-friend/$', views.tell_a_friend, name="tell_a_friend"),
    url(r'^newsletter/$', views.newsletter, name="newsletter"),
    url(r'^newsletter_send/$', views.newsletter_send, name="newsletter_send"),
)

