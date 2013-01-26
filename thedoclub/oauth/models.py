import bcrypt
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
    login = models.CharField(max_length=40, null=True)
    name = models.CharField(max_length=128, null=True)
    public_repos = models.IntegerField(null=True)
    
    def save(self, *args, **kwargs):
        if not self.secret_token:
            self.secret_token = self.generate_secret_token()
            
        super(GitHubUser, self).save(*args, **kwargs)
    
    def generate_secret_token(self):
        return bcrypt.hashpw(self.access_token, bcrypt.gensalt())
    
    def gh(self):
        return GitHub(access_token=self.access_token)
        
    def fetch_user_info(self):
        gh = self.gh()
        user = gh.user.get()
        
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

