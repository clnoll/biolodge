from django.forms import forms
from django.forms import fields

from django.contrib.gis.forms import fields as gis_fields


class RangeForm(forms.Form):
    mpoly = gis_fields.MultiPolygonField(label='')
