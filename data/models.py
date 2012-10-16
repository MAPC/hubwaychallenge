from django.contrib.gis.db import models
from django.utils.translation import ugettext as _

class Station(models.Model):

    id = models.IntegerField(primary_key=True)
    terminalname = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    installed = models.BooleanField()
    locked = models.BooleanField()
    installdate = models.DateTimeField(blank=True, null=True)
    removaldate = models.DateField(blank=True, null=True)
    temporary = models.BooleanField()
    lat = models.FloatField()
    lng = models.FloatField()

    point = models.PointField(geography=True, blank=True, null=True)

    objects = models.GeoManager()

    class Meta:
        ordering = ['id', ]
        verbose_name = _('Station')
        verbose_name_plural = _('Stations')

    def __unicode__(self):
        return self.terminalname
    

class Trip(models.Model):

    id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=20, null=True)
    duration = models.IntegerField(null=True)
    start_date = models.DateTimeField(null=True)
    start_station = models.ForeignKey(Station, related_name='start_station', null=True, blank=True)
    end_date = models.DateTimeField(null=True)
    end_station = models.ForeignKey(Station, related_name='end_station', null=True, blank=True)
    bike_nr = models.CharField(max_length=20, null=True)
    subscriber_id = models.IntegerField(null=True)
    subscription_type = models.CharField(max_length=20, null=True)
    zip_code = models.CharField(max_length=10, null=True)
    birth_date = models.IntegerField(null=True)
    gender = models.CharField(max_length=10, null=True)
    
    class Meta:
        verbose_name = _('Trip')
        verbose_name_plural = _('Trips')

    def __unicode__(self):
        return '%s' % (self.id)


class StationCapacity(models.Model):
    """ Aggregated from http://thehubway.com/data/stations/bikeStations.xml """
    
    id = models.IntegerField(primary_key=True)
    station = models.ForeignKey(Station)
    day = models.DateField()
    capacity = models.IntegerField()

    class Meta:
        verbose_name = _('Station capacity')
        verbose_name_plural = _('Station Capacities')

    def __unicode__(self):
        return '%s' % (self.id)