from django.contrib.gis import admin
from models import Station

try:
    _model_admin = admin.OSMGeoAdmin

    # default GeoAdmin overloads
    admin.GeoModelAdmin.default_lon = -7912100
    admin.GeoModelAdmin.default_lat = 5210000
    admin.GeoModelAdmin.default_zoom = 12
    
except AttributeError:
    _model_admin = admin.ModelAdmin

class StationAdmin(_model_admin):
    list_display = ('terminalname','name',)
    search_fields = ['terminalname','name',]
  
admin.site.register(Station,StationAdmin)
