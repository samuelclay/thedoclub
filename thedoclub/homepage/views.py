import datetime
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.conf import settings
from presentation.models import Presentation
from oauth.models import GitHubUser
from event.models import Event

def home(request):
    event = Event.objects.all()[0]
    secret_token = request.COOKIES.get('doclub_sessionid')
    attending = False
    
    if secret_token:
        try:
            user = GitHubUser.objects.get(secret_token=secret_token)
            attending = event.attendees.filter(id=user.id).exists()
        except GitHubUser.DoesNotExist:
            pass
    
    return render_to_response('homepage.html', {
        'settings': settings,
        'attending': attending,
        'event': event,
    }, context_instance=RequestContext(request))
