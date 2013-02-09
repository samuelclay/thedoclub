import json
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from oauth.models import GitHubUser
from oauth.tasks import github_fetcher
from vendor.github import GitHub
from vendor import github
from utils import github_login_required

def start(request):
    next = request.GET.get('next')

    return render_to_response('oauth_start.html', {
        'next': next,
    }, context_instance=RequestContext(request))
    
def authorize(request):
    next = request.GET.get('next')
    gh = GitHub(client_id=settings.GITHUB_CLIENT_ID, 
                client_secret=settings.GITHUB_CLIENT_SECRET)
    url = gh.authorize_url(state='thedoclub')
    
    response = HttpResponseRedirect(url)
    
    if next:
        response.set_cookie('oauth_next', next)
        
    return response
    
def callback(request):
    gh = GitHub(client_id=settings.GITHUB_CLIENT_ID, 
                client_secret=settings.GITHUB_CLIENT_SECRET)
    code = request.GET['code']
    state = request.GET['state']
    
    try:
        access_token = gh.get_access_token(code, state)
    except github.ApiAuthError:
        return HttpResponseRedirect(reverse('oauth-authorize'))
    
    user, _ = GitHubUser.objects.get_or_create(access_token=access_token)
    for repo in user.repos.all():
        repo.clear_languages()
    github_fetcher.delay(access_token=access_token)

    response = HttpResponseRedirect(reverse("oauth-status"))
    response.set_cookie('doclub_sessionid', user.secret_token, 
                        domain=settings.SESSION_COOKIE_DOMAIN)
    
    return response

def end(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    next = request.COOKIES.get('oauth_next', '/')
    
    return render_to_response('oauth_end.html', {
        'code': code,
        'state': state,
        'next': next,
    }, context_instance=RequestContext(request))
    
@github_login_required
def status(request):
    repos = request.ghuser.repos.all()
    finished_repos = len([r for r in repos if r.languages])
    next = request.COOKIES.get('oauth_next', '/')
    
    return HttpResponse(json.dumps({
        "repo_count": len(repos),
        "finished_repos": finished_repos,
        "failed_user_fetch": request.ghuser.failed_user_fetch,
        "failed_repo_fetch": request.ghuser.failed_repo_fetch,
        "next": next,
    }), mimetype="application/json")