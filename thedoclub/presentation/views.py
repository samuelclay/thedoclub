import datetime
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core.urlresolvers import reverse
from presentation.models import Presentation
from oauth.models import GitHubRepo
from utils import github_login_required


@github_login_required
def choose(request):
    request.ghuser.fetch_repos()
    
    return render_to_response('presentation_choose.html', {
        'ghuser': request.ghuser,
        'settings': settings,
    }, context_instance=RequestContext(request))

@github_login_required
def choose_confirm(request, repo_id):
    repo = get_object_or_404(GitHubRepo, repo_id=repo_id)
    
    presentation, _ = Presentation.objects.get_or_create(user=request.ghuser, repo=repo)
    presentation.build_slides()
    
    return HttpResponseRedirect(reverse('presentation-edit', kwargs={'repo_id': repo.repo_id}))

@github_login_required
def edit(request, repo_id):
    repo = get_object_or_404(GitHubRepo, repo_id=repo_id)
    
    return render_to_response('presentation_edit.html', {
        'presentation': repo.presentation,
        'repo': repo,
        'ghuser': request.ghuser,
        'settings': settings,
    }, context_instance=RequestContext(request))

def view(request, repo_id):
    repo = get_object_or_404(GitHubRepo, repo_id=repo_id)    

    return render_to_response('presentation_view.html', {
        'presentation': repo.presentation,
        'repo': repo,
        'settings': settings,
    }, context_instance=RequestContext(request))