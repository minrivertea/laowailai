# python
import datetime

# django
from django.db.models import Q
from django.conf import settings

# app
from laowailai.questions.models import Question
from laowailai.questions.split_search import split_search

STOPWORDS = (
      "a", "and", "are", "as", "at", "be", "but", "by",
      "for", "if", "in", "into", "is", "it",
      "no", "not", "of", "on", "or", "such",
      "that", "the", "their", "then", "there", "these",
      "they", "this", "to", "was", "will", "with"
      )


def find_questions(q=None, skip_photoless=False, city=None,
                default_find_all=False, split_searchterm=False, qs=None,
                **parameters):
    """return an queryset of Questions by searching the core frock. 
    
    The parameters are expected to be known attributes such as 'colour' or 
    'material'. The values for the parameters are only a primitive matching type
    (e.g. string) or a list/tuple each with valid primitive matching type.
    
    If 'default_find_all' is True, the default thing is to return all frocks. If
    not you have to provide at least a search string or a list of parameters.
    
    If 'every_word' is True, then searching for multiple words every word
    must match every word or the whole thing together.
    
    """
    int_attributes = ('bust', 'waist', 'hips',)
    float_attributes = ('price',)
    string_attributes = ('size_uk','designer', 'label', 'material', 'colour', 'title')
    
    if qs is None:
        qs = Question.objects.filter(city=city)

    if q is not None:
            
        # Now, convert what we can convert of the search term into 
        # parameters
        q = q.strip()
   
        aliases = {'size':'size_uk'}
        possible_parameters = int_attributes + float_attributes + string_attributes + \
                              ('type', 'category') + tuple(aliases.keys())
        
        q, q_parameters = split_search(q, possible_parameters)
        for real, alias in aliases.items():
            if alias in q_parameters:
                q_parameters[real] = q_parameters.pop(alias)
                
        parameters.update(q_parameters)
        
        if not split_searchterm:
            qset = Q(question__icontains=q) | \
                Q(description__icontains=q)
            
            qs = qs.filter(qset)
            
        # if the search term was 'ralph lauren', the above qset will contain 
        # things like
        #  designer__iexact="ralph lauren"
        # But what if the search was "black chanel" then you need to find it 
        # by doing colour__iexact="black" OR designer__iexact="chanel"
        # So, to be safe we have to search by all of them, e.g.:
        #  designer__iexact="ralph lauren" OR
        #  designer__iexact="ralph" OR
        #  designer__iexact="lauren" OR
        #  colour__iexact="ralph lauren" OR
        #  colour__iexact="ralph" OR
        #  colour__iexact="lauren" 
                
        if split_searchterm and len(q.split()) > 1:
            qset = None
            for word in q.split():
                if word.lower() in STOPWORDS:
                    continue
                
                
                
                if qset is None:
                    qset = Q(corefrock__material__iexact=word) | \
                           Q(corefrock__colour__name__iexact=word) | \
                           Q(corefrock__designer__iexact=word) | \
                           Q(corefrock__label__iexact=word) | \
                           Q(corefrock__category__name__iexact=word) | \
                           Q(corefrock__type__name__iexact=word) | \
                           Q(corefrock__title__icontains=word)
                else:
                    qset = qset | \
                           Q(corefrock__material__iexact=word) | \
                           Q(corefrock__colour__name__iexact=word) | \
                           Q(corefrock__designer__iexact=word) | \
                           Q(corefrock__label__iexact=word) | \
                           Q(corefrock__category__name__iexact=word) | \
                           Q(corefrock__type__name__iexact=word) | \
                           Q(corefrock__title__icontains=word)

                qs = qs.filter(qset)
        
    # If you don't pass any parameters or search question you get nothing
    if not default_find_all and not q and not parameters:
        return qs.filter(pk=-1)

    def _ok_int(x):
        try:
            return int(x)
        except ValueError:
            return None

    def _ok_float(x):
        try:
            return float(x)
        except ValueError:
            return None

    def _ok_string(x):
        try:
            return unicode(x).strip()
        except TypeError:
            return None
    
    def check_parameter_attributes(qs, attributes, type_):
                    
        if type_ is int:
            check_function = _ok_int
        elif type_ is float:
            check_function = _ok_float
        elif type_ in (basestring, unicode, str):
            check_function = _ok_string
    
        for attr in attributes:
            if attr in parameters:
                value = parameters.pop(attr)
                if isinstance(value, (tuple, list)):
                    value = [check_function(x) for x in value
                             if check_function(x) is not None]
                    if value:
                        # some of the values in this list were ok
                        if type_ in (basestring, unicode, str):
                            # need to use a Q
                            qset = None
                            for each in value:
                                # http://groups.google.com/group/django-users/browse_thread/thread/f9b7e3ef99958bd6
                                if qset is None:
                                    qset = Q(**{'corefrock__%s__iexact' % attr: each})
                                else:
                                    qset = qset | Q(**{'corefrock__%s__iexact' % attr: each})
                            qs = qs.filter(qset)
                        else:
                            qs = qs.filter(**{'corefrock__%s__in' % attr: value})
                    else:
                        qs = qs.filter(pk=-1) # this will never match
                else:
                    value = check_function(value)
                    if value is None:
                        # if you supply an invalid value you should 
                        # not expect to get anything back
                        qs = qs.filter(pk=-1) # this will never match
                    elif type_ in (basestring, unicode, str):
                        qs = qs.filter(**{'corefrock__%s__iexact' % attr: value})
                    else:
                        qs = qs.filter(**{'corefrock__%s' % attr: value})
                        
        return qs
                        
    qs = check_parameter_attributes(qs, int_attributes, int)

    qs = check_parameter_attributes(qs, float_attributes, float)
    
    qs = check_parameter_attributes(qs, string_attributes, basestring)
    
    if 'type' in parameters:
        value = parameters.pop('type')
        if isinstance(value, (tuple, list)):
            value = [_ok_string(x) for x in value if _ok_string(x)]
            if value:
                qset = None
                for each in value:
                    if qset is None:
                        qset = Q(corefrock__type__name__iexact=each)
                    else:
                        qset = qset | Q(corefrock__type__name__iexact=each)
                qs = qs.filter(qset)
            else:
                # no valid strings in the list of frock types
                qs = qs.filter(pk=-1)
        else:
            value = _ok_string(value)
            if value is None:
                # invalid value
                qs = qs.filter(pk=-1)
            else:
                qs = qs.filter(corefrock__type__name__iexact=value)
                
    if 'value' in parameters:
        value = parameters.pop('value')
        if isinstance(value, (tuple, list)):
            value = [_ok_string(x) for x in value if _ok_string(x)]
            if value:
                qset = None
                for each in value:
                    if qset is None:
                        qset = Q(corefrock__category__name__iexact=each)
                    else:
                        qset = qset | Q(corefrock__category__name__iexact=each)
                qs = qs.filter(qset)
            else:
                # no valid strings in the list of frock types
                qs = qs.filter(pk=-1)
        else:
            value = _ok_string(value)
            if value is None:
                # invalid value
                qs = qs.filter(pk=-1)
            else:
                qs = qs.filter(corefrock__category__name__iexact=value)
                
    if 'coming_soon' in parameters:
        value = parameters.pop('coming_soon')
        if value:
            # the frock must have a coming_soon and it must be something
            # in the future
            qs = qs.filter(coming_soon_date__isnull=False, 
                           coming_soon_date__gt=datetime.datetime.today())
        else:
            
            # coming_soon date must be null or past
            qset = Q(coming_soon_date__isnull=True) | \
                   Q(coming_soon_date__lte=datetime.datetime.today())
            qs = qs.filter(qset)
                

    # If you have default_find_all to be False and there are parameters
    # left that means that you have provided invalid keys and this should
    # not be allowed.
    if not default_find_all and parameters.keys():
        raise ValueError, "Used unrecognized keys: %s" % str(parameters.keys())
        #return qs.filter(pk=-1)

        
    # if there was a searchterm (q) and nothing was found, then
    # repeat the find_frocks() but with split_searchterm being True
    if q and len(q.split()) > 1 and not split_searchterm and \
      [w for w in q.split() if w.lower() not in STOPWORDS] and not qs.count():
        # getting desperate
        qs = find_frocks(split_searchterm=True,
                         q=q,
                         skip_photoless=skip_photoless,
                         default_find_all=default_find_all,
                         **parameters)
        
    if skip_photoless:
        raise NotImplementedError, "Feature not implemented yet"

    return qs
    
    

    
    
