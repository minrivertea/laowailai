from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from prowlpy import Prowl


def new_laowai(sender, instance, **kwargs):
    apikey = settings.PROWL_API_KEY
    p = Prowl(apikey)
    try:
        p.add(
            'laowailai.com',
            'New Laowai',
            'A new user just registered',
        )
    except Exception,msg:
        print msg
        
        

def new_subscriber(sender, instance, **kwargs):
    apikey = settings.PROWL_API_KEY
    p = Prowl(apikey)
    try:
        p.add(
            'laowailai.com',
            'New Subscriber',
            'A new subscriber just registered',
        )
    except Exception,msg:
        print msg
        
        


def comment_notifier(sender, comment, **kwargs):

    # this sends an email to the post-owner when someone comments on it.
    if comment.is_public:
        # find out the commenter and the info object
        from models import Laowai, Info
        info = get_object_or_404(Info, id=comment.object_pk)
        receiver = get_object_or_404(Laowai, id=info.added_by.id)
        commenter = get_object_or_404(Laowai, name=comment.user_name)
        
        if receiver != commenter:
        
            # define the content of the email
            subject = "New comment by %s on %s" % (
                comment.user_name,
                Site.objects.get_current().domain)
            body = render_to_string(
                "emails/comment_notifier.txt", {
                    'comment': comment.comment,
                    'commenter': commenter.name,
                    'post_url': info.get_absolute_url(),
                    })
        
            # send the email
            send_mail(
                              subject, 
                              body, 
                              'mail@laowailai.com',
                              [receiver.user.email], 
                              fail_silently=False
            )
        
        else:
            pass

 
