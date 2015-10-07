"""
Example region table:


| pk | name           | Polygon                       | modifier | is_fill | parent_region_1 | parent_region_2 |
|----+----------------+-------------------------------+----------+---------+-----------------+-----------------|
|  1 | Sulawesi       | "(1.1, 23.2),(1.7,23,5),..."  | null     | false   | null            | null            |
|  2 | India          | "(1.4, 23.2),(1.7,23,5),..."  | null     | false   | null            | null            |
|  3 | China          | "(10.5, 23.2),(1.7,23,5),..." | null     | false   | null            | null            |
|  4 | SEChina        | null                          | SE       | false   | 3               | null            |
|  5 | IndiaToChina   | null                          | null     | true    | 2               | 3               |
|  6 | IndiaToSEChina | null                          | null     | true    | 2               | 4               |
"""
from django.contrib.gis.db import models as gis_models
from django.db import models

from jsonfield import JSONField
import operator
from geo.models import WorldBorder


class Region(models.Model):

    name = models.CharField(null=False, unique=True, max_length=50)
    polygon = models.TextField()

    # E.g. northern, southeastern
    # non-null implies non-null parent_1
    # TODO: how to represent field with small set of valid choices {'n', 'se', ...}
    modifier = models.CharField(null=True, max_length=2)

    # true if region is a fill between two parent regions
    # true implies non-null parent_1 and parent_2
    is_fill = models.BooleanField()

    parent_1 = models.ForeignKey('Region', null=True, related_name='+')
    parent_2 = models.ForeignKey('Region', null=True, related_name='+')


class Bird(models.Model):

    order = models.CharField(max_length=100)
    family = models.CharField(max_length=100)
    genus = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    subspecies = models.CharField(max_length=100, null=True, blank=True)
    raw_range = models.TextField()
    parsed_range = models.TextField()
    ebird_id = models.CharField(max_length=100)
    common_name = models.CharField(max_length=100)

    regions = models.ManyToManyField(Region)

    mpoly = gis_models.MultiPolygonField(null=True)
    objects = gis_models.GeoManager()

    @property
    def is_valid(self):
        if self.parsed_range == '' or self.common_name == '':
            return False
        return True

    def _get_map_data(self):
        world_borders = {
            border.name.lower(): border
            for border in WorldBorder.objects.all()
        }

        if 'region_atoms' in self.parsed_range:
            bird_regions = set(self.parsed_range['region_atoms'])

            matched_regions = bird_regions & set(world_borders)
            unmatched_regions = bird_regions - set(world_borders)

            if matched_regions:
                bird_borders = [world_borders[region_name]
                                for region_name in matched_regions]

                mpolys = reduce(operator.add, (border.mpoly
                                               for border in bird_borders))
                return mpolys
        else:
            return None
