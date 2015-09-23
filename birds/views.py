from django.shortcuts import render
from rest_framework import generics
from rest_framework.serializers import ModelSerializer

from birds.forms import MapForm
from birds.models import Bird


class BirdSerializer(ModelSerializer):
    class Meta:
        model = Bird


class Birds(generics.ListAPIView):
    queryset = Bird.objects.all()
    serializer_class = BirdSerializer


def map_view(request):
    data = {
        'form': MapForm(),
    }
    return render(request, 'birds/map.html', data)
