from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from oauth.models import GitHubUser
from vendor.github import GitHub
from vendor import github

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
    user.fetch_user_info()

    next = request.COOKIES.get('oauth_next', '/')
    response = HttpResponseRedirect(next)
    response.set_cookie('doclub_sessionid', user.secret_token)
    
    return response