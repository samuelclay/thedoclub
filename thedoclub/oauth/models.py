import json
import bcrypt
import datetime
import iso8601
from django.db import models
from vendor.github import GitHub


class GitHubUser(models.Model):
    access_token = models.CharField(max_length=40, unique=True)
    secret_token = models.CharField(max_length=128, db_index=True)
    avatar_url = models.CharField(max_length=1024, null=True)
    bio = models.CharField(max_length=1024, null=True)
    blog = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    followers = models.IntegerField(null=True)
    following = models.IntegerField(null=True)
    hireable = models.BooleanField(default=False)
    github_id = models.CharField(max_length=40, null=True)
    location = models.CharField(max_length=255, null=True)
    login = models.CharField(max_length=40, null=True, db_index=True)
    name = models.CharField(max_length=128, null=True)
    public_repos = models.IntegerField(null=True)
    repo_refresh_date = models.DateTimeField(null=True)
    failed_user_fetch = models.BooleanField(default=False)
    failed_repo_fetch = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % (self.login)
        
    def save(self, *args, **kwargs):
        if not self.secret_token:
            self.secret_token = self.generate_secret_token()
            
        super(GitHubUser, self).save(*args, **kwargs)
    
    def generate_secret_token(self):
        return bcrypt.hashpw(self.access_token, bcrypt.gensalt())
    
    def gh(self):
        return GitHub(access_token=self.access_token)
    
    def fetch_user_info(self):
        try:
            gh = self.gh()
            user = gh.user.get()
            
            self.failed_user_fetch = False
            self.avatar_url = user['avatar_url']
            self.bio = user['bio']
            self.blog = user['blog']
            self.email = user['email']
            self.followers = user['followers']
            self.following = user['following']
            self.hireable = user['hireable']
            self.github_id = user['id']
            self.location = user['location']
            self.login = user['login']
            self.name = user['name']
            self.public_repos = user['public_repos']
        
            self.save()
        except Exception, e:
            print " ***> Failed user fetch: %s / %s" % (self, e)
            self.failed_user_fetch = True
            self.save()
    
    def fetch_repos(self, force=False, delay=False):
        try:
            gh = self.gh()
        
            day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
            if not force and self.repo_refresh_date and self.repo_refresh_date > day_ago:
                return
        
            if delay and not force:
                # FetchRepos.apply_async(kwargs={"login": self.login})
                return
            
            user_repos = gh.user.repos.get()
            self.failed_repo_fetch = False
            self.repo_refresh_date = datetime.datetime.now()
            self.save()
        
            GitHubRepo.create(self, user_repos)
            orgs = gh.user.orgs.get()
            for org in orgs:
                print " ---> Fetching org repos: %s / %s" % (self, org['login'])
                org_repos = gh.orgs(org['login']).repos.get()
                GitHubRepo.create(self, org_repos, org=org)
        
            for repo in self.repos.all():
                print " ---> Fetching repo languages: %s / %s" % (self, repo)
                try:
                    repo.fetch_languages()
                except:
                    print " ---> Failed repo language fetch: %s" % repo
                    pass
        except Exception, e:
            print " ***> Failed repo fetch: %s / %s" % (self, e)
            self.failed_repo_fetch = True
            self.save()


class GitHubRepo(models.Model):
    user = models.ForeignKey(GitHubUser, related_name='repos')
    owner_name = models.CharField(max_length=255, null=True)
    organization_id = models.IntegerField(null=True)
    organization_name = models.CharField(max_length=255, null=True)
    avatar_url = models.CharField(max_length=1024, null=True)
    description = models.CharField(max_length=1024, null=True)
    html_url = models.CharField(max_length=1024, null=True)
    repo_id = models.IntegerField(null=True)
    name = models.CharField(max_length=255, null=True)
    watchers = models.IntegerField(null=True)
    forks = models.IntegerField(null=True)
    pushed_at = models.DateTimeField(null=True)
    languages = models.CharField(max_length=1024, null=True)
    
    class Meta:
        ordering = ['organization_name', '-pushed_at']
        
    def __unicode__(self):
        return "[%s] %s (%s/%s)" % (self.organization_name 
                                    if self.organization_name else self.user.login,
                                    self.name, self.watchers, self.forks)
        
    @classmethod
    def create(cls, user, repos, org=None):
        avatar_url = user.avatar_url
        org_name = None
        org_id = None
        if org:
            org_name = org['login']
            org_id = org['id']
            avatar_url = org['avatar_url']
        for repo in repos:
            if repo['private']: continue
            
            ghrepo, _ = cls.objects.get_or_create(**{
                "user": user,
                "organization_id": org_id,
                "organization_name": org_name,
                "repo_id": repo['id'],
                "name": repo['name'],
            })
            ghrepo.owner_name = org_name or repo['owner']['login']
            ghrepo.description = repo['description']
            ghrepo.html_url = repo['html_url']
            ghrepo.watchers = repo['watchers']
            ghrepo.forks = repo['forks']
            ghrepo.avatar_url = repo['owner']['avatar_url']
            ghrepo.pushed_at = iso8601.parse_date(repo['pushed_at']).replace(tzinfo=None)
            ghrepo.save()
    
    def fetch_languages(self):
        gh = self.user.gh()
        
        languages = gh.repos('%s/%s' % (self.owner_name, self.name)).languages.get()
        total = sum(languages.values()) * 1.0
        languages_list = [(lang, score / total) for lang, score in languages.items()]
        languages_list = sorted(languages_list, key=lambda l: l[1], reverse=True)[:3]
        self.languages = json.dumps(languages_list)
        self.save()
    
    def clear_languages(self):
        self.languages = None
        self.save()
        
    @property
    def language_list(self):
        return json.loads(self.languages)
