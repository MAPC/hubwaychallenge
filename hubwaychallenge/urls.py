from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from django.conf import settings

# API
from tastypie.api import Api
from hubwaychallenge.api import StationResource, TripResource, StationCapacityResource, StationStatusResource

v1_api = Api(api_name='v1')
v1_api.register(StationResource())
v1_api.register(TripResource())
v1_api.register(StationCapacityResource())
v1_api.register(StationStatusResource())

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'hubwaychallenge.views.home', name='home'),
    (r'^register/$', TemplateView.as_view(template_name='register.html')),
    # url(r'^hubwaychallenge/', include('hubwaychallenge.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),

    # API urls
    (r'^api/', include(v1_api.urls)),

    # Social Auth
    url(r'', include('social_auth.urls')),
    # url(r'^login/$', redirect_to, {'url': '/login/github'}),
    # url(r'^private/$', 'home.views.private'),
    url(r'^logout/$', 'hubwaychallenge.views.logout_view', name='logout'),
    (r'^login-error/$', TemplateView.as_view(template_name='login-error.html')),
    url(r'^data-api/$', 'hubwaychallenge.views.data_api', name='data-api'),

    (r'^submission/', include('submission.urls')), 
    # leaderboard shortcut
    (r'^leaderboard/', RedirectView.as_view(url='/submission/leaderboard/')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True, }),
)
