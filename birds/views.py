from django.shortcuts import render
from rest_framework import generics
from rest_framework.serializers import ModelSerializer

from birds.forms import RangeForm
from birds.models import Bird
from geo.models import WorldBorder


class BirdSerializer(ModelSerializer):
    class Meta:
        model = Bird


class Birds(generics.ListAPIView):
    queryset = Bird.objects.all()
    serializer_class = BirdSerializer


def map_view(request):
    region = WorldBorder.objects.get(name='Indonesia')
    form = RangeForm(data={
        'name': region.name,
        'mpoly': region.mpoly,
    })
    return render(request, 'birds/map.html', {'form': form})
