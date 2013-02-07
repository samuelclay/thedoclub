from django.db import models
from oauth.models import GitHubRepo, GitHubUser
from presentation.models import Presentation


class Event(models.Model):
    starts_at = models.DateTimeField(null=True)
    location = models.CharField(max_length=255, null=True)
    attendees = models.ManyToManyField(GitHubUser)
    presentations = models.ManyToManyField(Presentation)
    
    class Meta:
        ordering = ['-starts_at']
    
    def __unicode__(self):
        return "%s: %s (%s attendees, %s presentations)" % (
            self.starts_at.strftime('%Y-%m-%d'), 
            self.location,
            self.attendees.count(),
            self.presentations.count(),
        )