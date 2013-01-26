import datetime
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.conf import settings
from presentation.models import Presentation
from utils import github_login_required


@github_login_required
def create(request):
    presentation = Presentation.create(user=request.ghuser)
    
    return HttpResponseRedirect(presentation.absolute_url('choose'))

@github_login_required
def choose(request, presentation_uuid):
    presentation = get_object_or_404(Presentation, url=presentation_uuid)
    
    request.ghuser.fetch_repos()
    
    return render_to_response('presentation_choose.html', {
        'presentation': presentation,
        'ghuser': request.ghuser,
        'settings': settings,
    }, context_instance=RequestContext(request))

@github_login_required
def edit(request, presentation_uuid):
    presentation = get_object_or_404(Presentation, url=presentation_uuid)
    
    return render_to_response('presentation_edit.html', {
        'presentation': presentation,
        'ghuser': request.ghuser,
        'settings': settings,
    }, context_instance=RequestContext(request))

def view(request, presentation_uuid):
    presentation = get_object_or_404(Presentation, url=presentation_uuid)
    
    return render_to_response('presentation_view.html', {
        'presentation': presentation,
        'settings': settings,
    }, context_instance=RequestContext(request))