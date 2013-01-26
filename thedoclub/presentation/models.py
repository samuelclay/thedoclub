from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
import hashlib
import uuid
import random
import datetime


class Presentation(models.Model):
    url = models.CharField(max_length=6, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    github_user_id = models.CharField(max_length=40)
    github_url = models.CharField(max_length=256, null=True, blank=True)
    is_submitted = models.BooleanField(default=False)
    
    def absolute_url(self):
        return '/round/%s' % self.url
    
    @classmethod
    def generate_url(cls):
        # XXX TODO: check for collision
        url = unicode(uuid.uuid4())[:6]
        return url