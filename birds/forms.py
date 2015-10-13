from django.contrib.gis import forms


class RangeForm(forms.Form):
    mpoly = forms.MultiPolygonField(label='')
