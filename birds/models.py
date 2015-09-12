from django.db import models


class Region(models.Model):

    name = models.CharField(null=False, unique=True, max_length=50)
    polygon = models.TextField()

    filled_from = models.ManyToManyField(Region)


class Subspecies(models.Model):

    order = models.CharField(max_length=50)
    family = models.CharField(max_length=50)
    genus = models.CharField(max_length=50)
    species = models.CharField(max_length=50)
    subspecies = models.CharField(max_length=50)
    raw_range = models.TextField()
    ebird_id = models.CharField(max_length=50)
    common_name = models.CharField(max_length=50)

    regions = models.ManyToManyField(Region)
