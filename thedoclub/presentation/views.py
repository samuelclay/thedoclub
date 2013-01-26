import datetime
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.conf import settings
from presentation.models import Presentation

def create(request):
    presentation = Presentation.objects.create(url=Presentation.generate_url())
    
    return HttpResponseRedirect(presentation.absolute_url())

def edit(request, presentation_uuid):
    presentation = get_object_or_404(Presentation, url=presentation_uuid)
    
    return render_to_response('presentation_edit.html', {
        'presentation': presentation,
        'settings': settings,
    }, context_instance=RequestContext(request))