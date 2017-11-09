from django.shortcuts import render
import math

import settings
import apps.search.settings

from django.contrib.auth.decorators import login_required
from apps.utils.utils import crop, t_metadata, t_log
from apps.utils.services import *
from apps.utils.views import *



@login_required
def index(request):

    t = get_ts_session(request)
    if isinstance(t,HttpResponse) :
        return error_view(request,t)

    q = request.GET.get('q')
    r = request.GET.get('r') if 'r' in request.GET else 10
    s = request.GET.get('s') if 's' in request.GET else 0

    #TODO clean input
    results = t.fulltext_search(request, {'query': q, 'type': 'LinesLc', 'rows': r, 'start' : s})
    if isinstance(results,HttpResponse):
        return apps.utils.views.error_view(request,results)

    collections = t.collections(request) #should be unecessary as collections are in request.session... but they are all wierded up
    if isinstance(collections,HttpResponse):
        return apps.utils.views.error_view(request,collections)

    t_log("%s" % results, logging.WARN)
    user_cols = []
    for collection in collections :
        user_cols.append(collection.get('colId'))

    hits = sorted(results.get('pageHits').get('PageHit'), key=lambda k: k['pageNr']) 
    numResults = results.get('numResults')
    res_pages = math.ceil(int(numResults)/int(r))
    to = numResults if int(s)+int(r) > numResults else int(s)+int(r)
    active_p = int(s)/int(r)
    return render(request, 'search/homepage.html', {
		'results' : hits, 
		'user_cols': user_cols, 
		'num_results': numResults,
		'q_str': q,
		'from' : int(s),
		'to': int(to),
		'res_pages' : range(0,res_pages),
		'r' : int(r),
		'active_p' : int(active_p)
    } )
