from django.contrib.gis import forms


class RangeForm(forms.Form):
    name = forms.CharField()
    mpoly = forms.MultiPolygonField()
