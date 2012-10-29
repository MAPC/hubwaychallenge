import os.path

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
        return '%s from %s' % (self.id, self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('submission.views.detail', None, { 'id': self.id, })

    @models.permalink
    def get_approval_url(self):
        return ('submission.views.approve', None, { 'id': self.id, })

    def filename(self):
        return os.path.basename(self.file.name)

    def thumbnail_url(self):
        return '%s_tn%s' % (self.screenshot.url[:-4], self.screenshot.url[-4:])

    def overall_judgerating(self):
        return self.judgerating.get_rating()
    overall_judgerating.short_description = 'Judge Rating'

    def overall_publicrating(self):
        return self.userrating.get_rating()
    overall_publicrating.short_description = 'Public Rating'

class JudgeNote(models.Model):

    user = models.ForeignKey(User)
    entry = models.ForeignKey(Entry)
    note = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('JudgeNote')
        verbose_name_plural = _('JudgeNotes')

    def __unicode__(self):
        return '%s for %s' % (self.user, self.entry)
    

