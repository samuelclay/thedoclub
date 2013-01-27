import hashlib
import uuid
import random
import datetime
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from oauth.models import GitHubRepo, GitHubUser


class Presentation(models.Model):
    user = models.ForeignKey(GitHubUser)
    repo = models.ForeignKey(GitHubRepo, null=True)
    url = models.CharField(max_length=6, unique=True)
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    is_submitted = models.BooleanField(default=False)
    
    def absolute_url(self, url_type=None):
        if url_type == 'edit':
            return reverse('presentation-edit', kwargs={"presentation_uuid": self.url})
        elif url_type == 'choose':
            return reverse('presentation-choose', kwargs={"presentation_uuid": self.url})
        else:
            return reverse('presentation-view', kwargs={"presentation_uuid": self.url})
    
    @staticmethod
    def generate_url():
        # XXX TODO: check for collision
        url = unicode(uuid.uuid4())[:6]
        return url
        
    @classmethod
    def create(cls, user):
        presentation = cls.objects.create(user=user, url=cls.generate_url())
        for slide_number in range(5):
            slide_number += 1
            slide = Slide.objects.create(presentation=presentation, order=slide_number)
            slide.user = presentation.user
            slide.content = render_to_string('slides/slide%s.md' % slide_number, {
                
            })
            slide.save()
        
        return presentation
    
    def __unicode__(self):
        return "%s: %s" % (self.user, self.repo)


class Slide(models.Model):
    presentation = models.ForeignKey(Presentation, related_name='slides')
    order = models.IntegerField()
    content = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        return "%s: Slide #%s (%s bytes)" % (self.presentation, self.order, len(self.content))

