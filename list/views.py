# core python imports
from django.conf import settings
from django.core.urlresolvers import reverse
from datetime import timedelta, datetime
from PIL import Image
from cStringIO import StringIO
import os, md5
import smtplib

# stuff from my app
from models import *
from forms import InfoAddForm, UnsubscribeForm, SubscriberAddForm, ProfilePhotoUploadForm, TellAFriendForm, AddBioForm, SuggestionForm
from laowailai.cities.models import City
from laowailai.places.models import Place

# django stuff
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.utils import simplejson
from django import http
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.serializers.json import DjangoJSONEncoder




#render shortcut
def render(request, template, context_dict=None, **kwargs):
    return render_to_response(
        template, context_dict or {}, context_instance=RequestContext(request),
                              **kwargs
    )

def index(request, slug=None):  
    if not request.user.is_authenticated():
        cities = City.objects.all()
        return render(request, "list/index.html", locals()) 
    else:
        laowai = request.user.get_profile()
        url = reverse('news_feed', args=[laowai.city.slug])
        return HttpResponseRedirect(url)
    url = reverse('news_feed', args=[city.slug])
    return HttpResponseRedirect(url) 


# news feed for a particular city
def news_feed(request, slug):
    city = get_object_or_404(City, slug=slug) 
    objects_list = NewInfo.objects.filter(city=city).order_by('-date')    
    paginator = Paginator(objects_list, 10) # Show 10 infos per page
    
    # this is where we load some ajax stuff
    try:
        page = int(request.GET.get('page', '1'))

    except ValueError:
        page = 1
    
    if request.GET.get('xhr') and page > 1:
        infos = paginator.page(int(request.GET.get('page')))
        laowai = request.user.get_profile()
        objects_list = []
        for info in infos.object_list:
            objects_list.append(render_to_string('list/snippets/feed_li.html', {
                    'object': info,
                    'laowai': laowai,
            }, context_instance=RequestContext(request)))

        json =  simplejson.dumps(objects_list, cls=DjangoJSONEncoder)
        return HttpResponse(json, mimetype='application/json')
        

    # If page request (9999) is out of range, deliver last page of results.
    try:
        objects = paginator.page(page)
    except (EmptyPage, InvalidPage):
        objects = paginator.page(paginator.num_pages)
        
    if request.method == 'POST':
        form = InfoAddForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            if content == "Add something" or content == "":
                HttpResponseRedirect('/')
                
            contact_details = form.cleaned_data['contact_details']
            date = form.cleaned_data['date']
            location = form.cleaned_data['location']
            url = form.cleaned_data['related_url']
            
            # find or create the user
            try:
                laowai = get_object_or_404(Laowai, user=request.user)
            except:
                return HttpResponseRedirect('/not-authorised/')
            
            # ignore the extra inputs if they are just the default values
            if contact_details == "Your contact details?":
                contact_details = ""
            if location == "A location for this piece of news?":
                location = ""
            if url == "A related URL?":
                url = ""
            
            # create the new piece of info
            new = NewInfo.objects.create(
                                      content=content,
                                      contact_details=contact_details,
                                      location=location,
                                      date=date,
                                      related_url=url,
                                      added_by=laowai,
                                      )
            
            new.save()
            url = request.META.get('HTTP_REFERER','/')
            return HttpResponseRedirect(url)
         
        
        else:
            if form.non_field_errors():
                non_field_errors = form.non_field_errors()
            else:
                errors = form.errors
        
    
    else:
        infoform = InfoAddForm()
    
    return render(request, "list/news_feed.html", locals())


def laowai(request, id):
    this_laowai = get_object_or_404(Laowai, id=id)
    
    
    objects_list = NewInfo.objects.filter(owner=this_laowai).order_by('-date')
    paginator = Paginator(objects_list, 3) # Show 3 infos per page
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    # If page request (9999) is out of range, deliver last page of results.
    try:
        objects = paginator.page(page)
    except (EmptyPage, InvalidPage):
        objects = paginator.page(paginator.num_pages)
    
    # check if the user is authenticated - if they are, we have a city and laowai
    if request.user.is_authenticated():
        laowai = request.user.get_profile()
        city = laowai.city
        if this_laowai == laowai:
            pass
    
    # if not, there's no laowai, and the city belongs to the this_laowai
    else:
        laowai = None
        city = this_laowai.city
    
    # if you're viewing your own profile, nothing. Otherwise, increment the profile views count    
    if laowai and this_laowai == laowai:
        pass
    else:
        if this_laowai.profile_views == None:
            this_laowai.profile_views = 1
        else:
            this_laowai.profile_views += 1
            
        this_laowai.save()
        
    # gather up the list of infos for this laowai.    
    

    return render(request, 'list/laowai.html', locals())

@login_required
def post(request, slug):
    city = get_object_or_404(City, slug=slug) 
    laowai = request.user.get_profile()
    if request.method == 'POST':
        form = InfoAddForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            if content == "Add something":
                return HttpResponseRedirect('/')
                        
            # create the new piece of info
            new = NewInfo.objects.create(
                                      content=content,
                                      owner=laowai,
                                      city=city,
                                      )
            
            new.save()
            
            url = reverse('news_feed', args=[city.slug])
            return HttpResponseRedirect(url)
        
        else:
            if form.non_field_errors():
                non_field_errors = form.non_field_errors()
            else:
                errors = form.errors
        
    
    else:
        infoform = InfoAddForm()
    
    return render(request, 'list/post.html', locals())
            
def a_post(request, number):
    info = get_object_or_404(Info, id=number)
    return render(request, 'list/a_post.html', locals())


@login_required
def add_a_bio(request):
    if request.method == 'POST':
        form = AddBioForm(request.POST)
        if form.is_valid():
            this_laowai = get_object_or_404(Laowai, user=request.user)
            this_laowai.bio = form.cleaned_data['bio']
            this_laowai.save()
            
            url = reverse('laowai', args=[this_laowai.id])
            return HttpResponseRedirect(url)

    
    else:
        form = AddBioForm()
    
    return render(request, 'list/forms/add_bio.html', locals())

# GROUP : FORMS
def subscribe(request):
    if request.method == 'POST':
        form = SubscriberAddForm(request.POST)
        if form.is_valid():        
            email = form.cleaned_data['email'] 

            try:
                # check if they are already subscribed
                subscriber = get_object_or_404(Subscriber, email=email)
                # if they are, let them know and ignore request
                if subscriber:
                    message = "You're already subscribed to receive emails - if you haven't received any, let us know!"
                    return render(request, 'index.html', locals())
            except:
                #if not, add them            
                subscriber = Subscriber.objects.create(
                                      email=email,
                                      date_added=datetime.now(),
                                      )
                subscriber.save()
                
                # subscriber is saved now, let's send them a welcome email immediately
                body = render_to_string('list/emails/welcome_subscriber.txt', {
                    'email_address': subscriber.email,                                                 
                    })
                
                send_mail(
                          'LaoWaiLai - Thanks for Subscribing!', 
                          body, 
                          'chris@laowailai.com',
                          [subscriber.email], 
                          fail_silently=False
                )

            
            message = "Success! We'll be sending weekly emails to <strong>%s</strong> - you can unsubscribe at any time using the link in the footer." % subscriber.email
            return render(request, 'list/index.html', locals())

        else:
            if form.non_field_errors():
                non_field_errors = form.non_field_errors()
            else:
                errors = form.errors
    else:
        form = SubscriberAddForm()
    
    return render(request, 'list/subscribe.html', locals())
       


def unsubscribe(request):
    if request.method == 'POST':
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            email_address = form.cleaned_data['email']
            try:
                laowai = get_object_or_404(Laowai, user__email=email_address)
            except:
                try:
                    subscriber = get_object_or_404(Subscriber, email=email_address)
                    subscriber.active = False
                    subscriber.save()
                    return HttpResponseRedirect('/unsubscribe-successful/')
                except:
                    new_form = UnsubscribeForm()
                    return render(request, 'forms/unsubscribe.html', {
                    'message': "We don't have a record of this email address in our system.",
                    'email': form.cleaned_data['email'],
                    'form': new_form,
                    })
            
            laowai.subscribe = False
            laowai.save()
            return HttpResponseRedirect('/unsubscribe-successful/') 
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect('/user-unsubscribe/')
        
        form = UnsubscribeForm()
    
    return render(request, 'list/forms/unsubscribe.html', locals())

def user_unsubscribe(request):
    laowai = get_object_or_404(Laowai, user=request.user)
    laowai.subscribe = False
    laowai.save()
    message = "You've unsubscribed from receiving weekly emails, but you can still post news and events, and resubscribe at any time. Thanks!" 
    return render(request, 'list/index.html', locals())

def user_subscribe(request):
    laowai = get_object_or_404(Laowai, user=request.user)
    laowai.subscribe = True
    laowai.save()
    message = "You're subscribed to receive weekly emails. Thanks!" 
    return render(request, 'list/index.html', locals())
    
def tell_a_friend(request):
    if request.method == 'POST':
        form = TellAFriendForm(request.POST)
        if form.is_valid():
            try:
                the_sender = get_object_or_404(Laowai, user=form.cleaned_data['sender'])
            except:
                the_sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']
            recipient = form.cleaned_data['recipient']
            
            # create email
            if message:
                body = render_to_string('list/emails/custom_tell_friend.txt', {'message': message})
            else:
                body = render_to_string('list/emails/tell_friend.txt', {'sender': the_sender})
                
            send_mail(
                          'Check out LaoWaiLai Fuzhou', 
                          body, 
                          the_sender,
                          [recipient], 
                          fail_silently=False
            )
                        
            message = "We've sent an email to %s inviting them to the site - thanks!" % recipient
            return render(request, 'list/index.html', locals())

        else:
            if form.non_field_errors():
                non_field_errors = form.non_field_errors()
            else:
                errors = form.errors
             

    else:
        form = TellAFriendForm()
    return render(request, 'list/forms/tell_a_friend.html', locals())

# GROUP : FORM SUCCESS PAGES
    
def unsubscribe_successful(request):
    return render(request, 'list/unsubscribe_successful.html', locals())
    
def newsletter(request):
    if request.user.is_superuser:
        # evaluates if the infos were posted in the last week or not
        info_list = Info.objects.all().order_by('-date_added')
        infos = []
        for i in info_list:
            if not i.date_added < datetime.now() + timedelta(days = -7):
                infos.append(i)
        
        # get the current list of active subscribers
        subscribers = Subscriber.objects.filter(active=True)
        
        # get the current list of subscribed members
        registered_users = Laowai.objects.filter(subscribe=True)
        
        # join them all in one big happy list
        receivers = []
        for s in subscribers:
            receivers.append(s)
        for r in registered_users:
            receivers.append(r)
    
        return render(request, 'list/newsletter.html', locals())
    
    else:
        raise Http404

def newsletter_send(request):
    if request.user.is_superuser:
        # evaluates if the infos were posted in the last week or not
        info_list = Info.objects.all().order_by('-date_added')
        infos = []
        for i in info_list:
            if not i.date_added < datetime.now() + timedelta(days = -7):
                infos.append(i)
        
        # get the current list of active subscribers
        subscribers = Subscriber.objects.filter(active=True)
        
        # get the current list of subscribed members
        registered_users = Laowai.objects.filter(subscribe=True)
        
        # join them all in one big happy list
        receivers = []
        for s in subscribers:
            receivers.append(s)
        for r in registered_users:
            receivers.append(r)
            
        body = render_to_string('list/emails/newsletter.txt', {'infos': infos})
        
        for r in registered_users:
            recipient = r.user.email
            send_mail(
                "Fuzhou news from Laowailai.com",
                body,
                "mail@laowailai.com",
                [recipient],
                fail_silently=False
            )
        
        for r in subscribers: 
            recipient = r.email
            send_mail(
                "Fuzhou news from Laowailai.com",
                body,
                "mail@laowailai.com",
                [recipient],
                fail_silently=False
            )
    
        return render(request, 'list/newsletter_sent.html', locals())
    
    else:
        raise Http404


    
#GROUP : LIKES
@login_required
def like(request, item=None):
   
    if request.GET.get('xhr'):
        info = get_object_or_404(Info, id=request.GET.get('info'))
        laowai = get_object_or_404(Laowai, id=request.GET.get('laowai'))
        new_object = Likes.objects.create(liker=laowai, liked=info)
        message = "You like this"
        json =  simplejson.dumps(message, cls=DjangoJSONEncoder)
        return HttpResponse(json, mimetype='application/json')
        
    else:
        laowai = request.user.get_profile()
        info = get_object_or_404(Info, id=item)
        new_object = Likes.objects.create(liker=laowai, liked=info)

        return HttpResponseRedirect("/%s/feed/#info_%s" % (info.city.slug, info.id))

 

# GROUP : PROFILE UPDATE STUFF

def upload_profile_photo(request, next=None):
    if request.method == 'POST':
        form = ProfilePhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            laowai = get_object_or_404(Laowai, user=request.user)
            # Figure out what type of image it is
            photo = request.FILES['photo']
            image_content = photo.read()
            image = Image.open(StringIO(image_content))
            format = image.format
            format = format.lower().replace('jpeg', 'jpg')
            filename = md5.new(image_content).hexdigest() + '.' + format
            # Save the image
            path = os.path.join(settings.MEDIA_ROOT, 'photos/profiles', filename)
            # check that the dir of the path exists
            dirname = os.path.dirname(path)
            if not os.path.isdir(dirname):
                try:
                    os.mkdir(dirname)
                except IOError:
                    raise IOError, "Unable to create the directory %s" % dirname
            open(path, 'w').write(image_content)
            laowai.photo = 'photos/profiles/%s' % filename
            laowai.save()
            next = request.POST['next']
            return HttpResponseRedirect(next)


    else:
        form = ProfilePhotoUploadForm()
        url = request.META.get('HTTP_REFERER','/')
        next = url
    return render(request, 'list/forms/upload_profile_photo.html', locals())
    
    
def suggestions(request):
    suggestions = Suggestion.objects.all().order_by('date_added')
    
    # I want to check if they have already voted
    try:
        voted = request.session['VOTED']
    except:
        voted = "0"
        
    # if they have voted, I will show them a message
    if voted == "1":
        message = "Your vote has been counted - thanks!"
        request.session['VOTED'] = None
    
    # the usual handling if someone has submitted a suggestion
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            desc = form.cleaned_data['description']
            date = datetime.now()
            votes = 0
            try:
                laowai = get_object_or_404(Laowai, user=request.user)
            except:
                laowai = "Anonymous"
            
            suggestion = Suggestion.objects.create(
                        title=title,
                        description=desc,
                        date_added=date,
                        votes=votes,
                        submitted_by=laowai.name,                       
            )
            
            suggestion.save()
            
            return HttpResponseRedirect("/suggestions/")
    
    else:
        form = SuggestionForm()
    
    return render(request, 'list/suggestions.html', locals())
    

def suggestion_vote(request, suggestion):
    suggestion = get_object_or_404(Suggestion, id=suggestion)
    
    suggestion.votes += 1
    suggestion.save()
    
    request.session['VOTED'] = "1"
    
    url = request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(url)
#    suggestions = Suggestion.objects.all().order_by('date_added')
#    message = "Your vote has been counted - thanks!"
#    form = SuggestionForm()
#    return render(request, 'suggestions.html', locals())

def people(request, slug):
    if request.user.is_authenticated():
        laowai = request.user.get_profile()
    else:
        laowai = None
    
    city = get_object_or_404(City, slug=slug)       
    people = Laowai.objects.filter(city=city)        
    return render(request, "list/people.html", locals())


def ajax_comment(request):
    if request.GET.get('c'):
        from django.contrib.comments.models import Comment
        comment = get_object_or_404(Comment, pk=request.GET.get('c'))
        comment_html = render_to_string('snippets/comment.html', {'comment': comment})
        return HttpResponse(comment_html, mimetype='text/html')
    else:
       return False

@login_required
def whats_next(request):
    cities = City.objects.all()
    return render(request, "list/whats_next.html", locals())

@login_required
def set_city(request, slug):
    laowai = request.user.get_profile()
    city = get_object_or_404(City, slug=slug)
    laowai.city = city
    laowai.save()
       
    url = request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(url)

