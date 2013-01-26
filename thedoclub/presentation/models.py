from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
import hashlib
import uuid
import random
import datetime


class Presentation(models.Model):
    url = models.CharField(max_length=6, unique=True)
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    github_user_id = models.CharField(max_length=40)
    github_url = models.CharField(max_length=256, null=True, blank=True)
    is_submitted = models.BooleanField(default=False)
    
    def absolute_url(self, url_type=None):
        if url_type == 'edit':
            return reverse('presentation-edit', kwargs={"presentation_uuid": self.url})
        else:
            return reverse('presentation-view', kwargs={"presentation_uuid": self.url})
    
    @staticmethod
    def generate_url():
        # XXX TODO: check for collision
        url = unicode(uuid.uuid4())[:6]
        return url
        
    @classmethod
    def create(cls):
        presentation = cls.objects.create(url=cls.generate_url())
        for slide_number in range(5):
            slide_number += 1
            slide = Slide.objects.create(presentation=presentation, order=slide_number)
            slide.github_user_id = presentation.github_user_id
            slide.content = render_to_string('slides/slide%s.md' % slide_number, {
                
            })
            slide.save()
        
        return presentation


class Slide(models.Model):
    presentation = models.ForeignKey(Presentation, related_name='slides')
    github_user_id = models.CharField(max_length=40)
    order = models.IntegerField()
    content = models.TextField(null=True, blank=True)
    