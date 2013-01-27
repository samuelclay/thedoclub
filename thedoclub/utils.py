from django.http import HttpResponseRedirect
from oauth.models import GitHubUser

def github_login_required(function=None):
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            secret_token = request.COOKIES.get('doclub_sessionid')
            if not secret_token:
                return HttpResponseRedirect('/oauth/authorize?next=%s' % request.path)
            try:
                user = GitHubUser.objects.get(secret_token=secret_token)
            except GitHubUser.DoesNotExist:
                return HttpResponseRedirect('/oauth/authorize?next=%s' % request.path)
            
            setattr(request, 'ghuser', user)
            return view_func(request, *args, **kwargs)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)