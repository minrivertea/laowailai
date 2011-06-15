from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from fuzhounet.questions import views


urlpatterns = patterns('',
    url(r'^$', views.questions, name="questions"),
    url(r'^add/$', views.add_question, name="add_question"),
    url(r'^answer/([\w+])/$', views.vote, name="vote"),
    url(r'^(?P<slug>[\w-]+)/$', views.question, name="question"),
    url(r'^(?P<slug>[\w-]+)/add-answer/$', views.add_answer, name="add_answer"),

)

