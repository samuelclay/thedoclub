from celery import task
from oauth.models import GitHubUser


@task
def github_fetcher(access_token):
    user = GitHubUser.objects.get(access_token=access_token)
    user.fetch_user_info()
    user.fetch_repos()
