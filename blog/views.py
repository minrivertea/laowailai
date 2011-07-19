from blog.models import BlogEntry
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

#render shortcut
def render(request, template, context_dict=None, **kwargs):
    return render_to_response(
        template, context_dict or {}, context_instance=RequestContext(request),
                              **kwargs
    )

def index(request):
    entries = BlogEntry.objects.filter(is_draft=False).order_by('-date_added')[:10]                     
    return render(request, "blog/home.html", locals())
    
def more(request):
    entries = BlogEntry.objects.filter(is_draft=False).order_by('-date_added')  
    return render(request, "blog/more.html", locals())
    
def even_more(request):
    entries = BlogEntry.objects.all().filter(is_draft=False).order_by('-date_added')
    latest = []         
    for entry in entries:
        latest.append(dict(
                           date=entry.date_added,
                           type=entry.get_type(),
                           summary=entry.summary,
                           slug=entry.slug,
                           title=unicode(entry.title))
                           ) 
    latest_things = sorted(latest, reverse=True, key=lambda k: k['date']) 
    return render(request, "blog/even_more.html", locals())
    
@csrf_protect   
def blog_entry(request, slug):
    entry = get_object_or_404(BlogEntry, slug=slug)
    other_entries = BlogEntry.objects.exclude(id=entry.id).order_by('?')[:2] 
    return render(request, "blog/entry.html", locals())
  