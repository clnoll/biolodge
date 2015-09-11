from django.shortcuts import render
from django.views.generic import View
from rest_framework import generics
from rest_framework.serializers import ModelSerializer

from birds.models import Subspecies


class BirdSerializer(ModelSerializer):
    class Meta:
        model = Subspecies


class Birds(generics.ListAPIView):
    queryset = Subspecies.objects.all()
    serializer_class = BirdSerializer
