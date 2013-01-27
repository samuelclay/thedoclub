from django.db import models
from oauth.models import GitHubRepo, GitHubUser

# Create your models here.


class Event(models.Model):
    starts_at = models.DateTimeField(null=True)
    location = models.CharField(max_length=255, null=True)
    attendees = models.ManyToManyField(GitHubUser)
    repos = models.ManyToManyField(GitHubRepo)
    
    def __unicode__(self):
        return "%s: %s" % (self.starts_at, self.location)