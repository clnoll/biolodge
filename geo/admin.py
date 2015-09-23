from django.contrib.gis import admin
from geo.models import WorldBorder

admin.site.register(WorldBorder, admin.GeoModelAdmin)
