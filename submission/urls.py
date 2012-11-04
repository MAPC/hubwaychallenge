from django.conf.urls import patterns, include, url

from submission import views


urlpatterns = patterns('submission.views',
    url('^(?P<id>\d+)/$', 'detail', name='entry-detail'),
    url('^add/', 'add', name='add-entry'),
    url('^rate/(?P<id>\d+)$', 'rate', name='rate-entry'),
    url('^judgerate/(?P<id>\d+)$', 'judgerate', name='judgerate-entry'),
    url('^judgenote/', 'judgenote', name='judgenote'),
    url('^approve/(?P<id>\d+)$', 'approve', name='approve-entry'),
    url('^leaderboard/', 'leaderboard', name='leaderboard')
)