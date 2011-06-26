# core python imports
from django.conf import settings
from django.core.urlresolvers import reverse
from datetime import timedelta, datetime
from PIL import Image
from cStringIO import StringIO
import os, md5
import smtplib
import re

# stuff from my app
from laowailai.list.models import Laowai
from laowailai.questions.models import Question, Answer, Vote
from laowailai.questions.forms import AddQuestionForm, AddAnswerForm, SearchForm
from laowailai.questions.data import find_questions
from laowailai.slugify import get_slugify
from laowailai.cities.models import City


# django stuff
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf


#render shortcut
def render(request, template, context_dict=None, **kwargs):
    return render_to_response(
        template, context_dict or {}, context_instance=RequestContext(request),
                              **kwargs
    )

def questions(request, slug, qs=None, parameters={}):
    city = get_object_or_404(City, slug=slug)
        
    # if there's a search query
    if request.GET.get('q'):
        search_form = SearchForm(initial=request.GET)
        q = request.GET.get('q')
        questions = find_questions(q=q, qs=qs, city=city, **parameters)
        return render(request, "questions/questions.html", locals())
    else:
        search_form = SearchForm()
        
    questions = Question.objects.filter(is_published=True, city=city)

    return render(request, "questions/questions.html", locals())


def question(request, slug, questionslug):
    city = get_object_or_404(City, slug=slug)
    question = get_object_or_404(Question, slug=questionslug)
    if not question.is_published:
        return Http404()
    
    
    if request.user.is_authenticated():
        laowai = request.user.get_profile()
    else:
        laowai = None
        
    vote_list = Vote.objects.filter(laowai=laowai)
    answers_list = []
    for answer in Answer.objects.filter(question=question):
        if answer in (x.answer for x in vote_list):
            voted=True
        else:
            voted=False
        if answer.added_by == laowai:
            owner = True
        else: 
            owner = False
        answers_list.append(dict(answer=answer, voted=voted, owner=owner, vote_count=answer.vote_count))
    answers = sorted(answers_list, reverse=True, key=lambda k: k['vote_count'])
    
    return render(request, "questions/question.html", locals())

@login_required
def add_question(request, slug):
    city = get_object_or_404(City, slug=slug)
    
    if request.method == 'POST':
        form = AddQuestionForm(request.POST)
        if form.is_valid():
            laowai = request.user.get_profile()
            slug = get_slugify(form.cleaned_data['question'])
            while(Question.objects.filter(slug__iexact=slug).count()):
                current_number_suffix_match = re.search("\d+$", slug)
                current_number_suffix = current_number_suffix_match and current_number_suffix_match.group() or 0
                next = str(int(current_number_suffix) +1)
                slug = re.sub("(\d+)?$", next, slug)
            creation_args = {
                        'question': form.cleaned_data['question'],
                        'description': form.cleaned_data['description'],
                        'added_by': laowai,
                        'slug': slug,
                        'city': form.cleaned_data['city'],
            }
                     
            
            question = Question.objects.create(**creation_args)
            
            return HttpResponseRedirect('/questions/')
    else:
        form = AddQuestionForm()
    
    return render(request, "questions/forms/add_question.html", locals())

@login_required
def add_answer(request, slug, questionslug):
    question = get_object_or_404(Question, slug=questionslug)
    if request.method == 'POST':
        form = AddAnswerForm(request.POST)
        if form.is_valid():
            laowai = request.user.get_profile()
            creation_args = {
                'answer': form.cleaned_data['answer'],
                'added_by': laowai,
                'question': question,	
            }
            
            answer = Answer.objects.create(**creation_args)
            url = question.get_absolute_url()
            return HttpResponseRedirect(url)
    else:
        form = AddAnswerForm()
    
    return render(request, "questions/forms/add_answer.html", locals())

@login_required
def vote(request, id):
    answer = get_object_or_404(Answer, pk=id) 
    answer.vote_count += 1
    answer.save()
    
    laowai = get_object_or_404(Laowai, user=request.user)
    vote_obj = Vote.objects.create(
        answer=answer,
        laowai=laowai,
    )
    url = request.META.get('HTTP_REFERER','/')
    return HttpResponseRedirect(url)