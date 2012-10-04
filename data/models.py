from django.contrib.gis.db import models
from django.utils.translation import ugettext as _

class Station(models.Model):

    # -- IMPORT CSV DATA
    # COPY data_station(id,terminalName,name,installed,locked,installDate,removalDate,temporary,lat,lng)
    # FROM '/vagrant/hubwaychallenge/data/csv/stations.csv'
    # DELIMITERS ','
    # CSV HEADER;

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

    # -- IMPORT CSV DATA
    # COPY data_trip(id,status,duration,start_date,start_station_id,end_date,end_station_id,bike_nr,subscriber_id,subscription_type,zip_code,birth_date,gender)
    # FROM '/vagrant/hubwaychallenge/data/csv/trips-db-import.csv'
    # DELIMITERS ','
    # CSV HEADER;

    # replace 'nan' with ''
    # perl -pi -e 's/nan//g' trips-dbimport_.csv 

    # remove duplicate keys
    # awk -F, '(!X[$1]) {X[$1]=1; print $0}' trips-dbimport_.csv > trips-dbimport__.csv 

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
