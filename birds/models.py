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
from django.db import models

from jsonfield import JSONField
import operator


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
    parsed_range = JSONField()
    ebird_id = models.CharField(max_length=100)
    common_name = models.CharField(max_length=100)

    regions = models.ManyToManyField(Region)

    @property
    def mpoly(self):
        world_borders = {
            border.name.lower(): border
            for border in WorldBorder.objects.all()
        }
        region_world_borders = [world_borders[region_name]
                                for region_name in bird.matched_regions]

        bird_region = reduce(operator.add, (border.mpoly
                             for border in region_world_borders))

        return bird_region

    @property
    def matched_regions(self):
        if self.is_valid:
            return self._get_map_data()['matched_region']
        return []

    @property
    def unmatched_regions(self):
        if self.is_valid:
            return self._get_map_data()['unmatched_region']
        return []

    @property
    def is_valid(self):
        if self.parsed_range == '' or self.common_name == '':
            return False
        return True

    @staticmethod
    def _get_map_data(self):
        world_borders = {
            border.name.lower(): border
            for border in WorldBorder.objects.all()
        }

        bird_regions = set(self.parsed_range['region_atoms'])

        matched_regions = bird_regions & set(world_borders),
        unmatched_regions = bird_regions - set(world_borders),

        return {'matched_regions': matched_regions,
                'unmatched_regions': unmatched_regions}
