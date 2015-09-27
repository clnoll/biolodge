from django.shortcuts import render
from rest_framework import generics
from rest_framework.serializers import ModelSerializer

from birds.forms import RangeForm
from birds.models import Bird
from utils import get_map_data_from_birds


class BirdSerializer(ModelSerializer):
    class Meta:
        model = Bird


class Birds(generics.ListAPIView):
    queryset = Bird.objects.all()
    serializer_class = BirdSerializer


class BirdDetails(generics.DetailView):

    def get(self, request):
        bird_pks = self.kwargs['pk']

        data = {
            'birds': get_map_data_from_birds(birds=bird_pks),
            'form_media': RangeForm().media,
        }

        return render(request, 'birds/detail.html', data)
