from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource
from tastypie.resources import ALL
from tastypie.cache import SimpleCache
from tastypie.throttle import BaseThrottle
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.models import create_api_key

from data.models import Station, Trip, StationCapacity

from django.contrib.auth.models import User
from django.db import models

# create API key for each registered user
models.signals.post_save.connect(create_api_key, sender=User)


class StationResource(ModelResource):
    class Meta:
        queryset = Station.objects.all()
        resource_name = 'station'
        allowed_methods = ['get']
        cache = SimpleCache()
        limit = 100
        # throttle = BaseThrottle(throttle_at=3600)
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        excludes = ['lat','lng',]
        filtering = {
            'id': ALL,
            'terminalname': ALL,
            'name': ALL,
            'installed': ALL,
            'locked': ALL,
            'installdate': ALL,
            'removaldate': ALL,
            'temporary': ALL,
        }



class TripResource(ModelResource):

    start_station = fields.ToOneField('hubwaychallenge.api.StationResource', 'start_station')
    end_station = fields.ToOneField('hubwaychallenge.api.StationResource', 'end_station')

    class Meta:
        # tastypie doesn't allow null values in FK
        queryset = Trip.objects.filter(start_date__isnull=False, end_date__isnull=False)
        resource_name = 'trip'
        allowed_methods = ['get']
        cache = SimpleCache()
        limit = 100
        # throttle = BaseThrottle(throttle_at=3600)
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        excludes = ['subscriber_id',]
        filtering = {
            'id': ALL,
            'status': ALL,
            'duration': ALL,
            'start_date': ALL,
            'start_station': ALL,
            'end_date': ALL,
            'end_station': ALL,
            'bike_nr': ALL,
            'subscription_type': ALL,
            'zip_code': ALL,
            'birth_date': ALL,
            'gender': ALL,
        }


class StationCapacityResource(ModelResource):

    station = fields.ToOneField('hubwaychallenge.api.StationResource', 'station')

    class Meta:
        queryset = StationCapacity.objects.all()
        resource_name = 'stationcapacity'
        allowed_methods = ['get']
        cache = SimpleCache()
        limit = 100
        # throttle = BaseThrottle(throttle_at=3600)
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
            'id': ALL,
            'station': ALL,
            'day': ALL,
            'capacity': ALL,
        }
