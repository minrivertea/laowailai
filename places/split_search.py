#-*- coding: iso-8859-1 -*
## 
## Split search string - Useful when building advanced search application
## By: Peter Bengtsson, mail@peterbe.com
## May 2008
## ZPL
##

__version__='1.0'

"""

split_search(searchstring [str or unicode], 
                      keywords [list or tuple])
                      
  Splits the search string into a free text part and a dictionary of keyword 
  pairs. For example, if you search for 'Something from: Peter to: Lukasz' 
  this function will return 
  'Something', {'from':'Peter', 'to':'Lukasz'}
  
  It works equally well with unicode strings.
  
  Any keywords in the search string that isn't recognized is considered text.
  
"""

import re


def split_search(q, keywords):
    params = {}
    s = []
    
    regex = re.compile(r'\b(%s):' % '|'.join(keywords), re.I)
    bits = regex.split(q)
    
    skip_next = False
    for i, bit in enumerate(bits):
        if skip_next:
            skip_next = False
        else:
            if bit in keywords and params:
                params[bit.lower()] = bits[i+1].strip()
                skip_next = True
            elif bit.strip():
                s.append(bit.strip())
                
    return ' '.join(s), params

        
