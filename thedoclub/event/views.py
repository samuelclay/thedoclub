from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core.urlresolvers import reverse
from event.models import Event
from oauth.models import GitHubRepo
from utils import github_login_required

@github_login_required
def attend(request):
    
    event = Event.objects.order_by('-starts_at')[0]
    event.attendees.add(request.ghuser)
    
    return HttpResponseRedirect(reverse('home'))
