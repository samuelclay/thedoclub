import datetime
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.conf import settings
from presentation.models import Presentation

def home(request):
    
    return render_to_response('homepage.html', {
        'settings': settings,
    }, context_instance=RequestContext(request))
