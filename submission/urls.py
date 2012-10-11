from django.conf.urls import patterns, include, url

from submission import views


urlpatterns = patterns('submission.views',
    url('^(?P<id>\d+)/$', 'detail', name='entry-detail'),
    url('^add/', 'add', name='add-entry'),
)