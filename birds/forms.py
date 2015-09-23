from django.contrib.gis import forms
from django.contrib.gis.forms.fields import MultiPolygonField


class MapForm(forms.Form):
    mpoly = MultiPolygonField()
