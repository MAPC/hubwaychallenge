from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from djangoratings.fields import RatingField

# Create your models here.

class Entry(models.Model):
    """ A challenge submission entry. """

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    user = models.ForeignKey(User, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    screenshot = models.ImageField(upload_to='submission/screenshots')
    file = models.FileField(upload_to='submission/entries', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    rules = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    userrating = RatingField(range=5, can_change_vote=True)
    judgerating = RatingField(range=5, can_change_vote=True)

    class Meta:
        ordering = ['id']
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.email)

    @models.permalink
    def get_absolute_url(self):
        return ('submission.views.detail', None, { 'id': self.id, })

    @models.permalink
    def get_approval_url(self):
        return ('submission.views.approve', None, { 'id': self.id, })

