import operator

from django.shortcuts import render
from django.views.generic import View
from rest_framework import generics
from rest_framework.serializers import ModelSerializer

from birds.forms import RangeForm
from birds.models import Bird
from geo.models import WorldBorder


class BirdSerializer(ModelSerializer):
    class Meta:
        model = Bird


class BirdListAPIView(generics.ListAPIView):
    queryset = Bird.objects.all()
    serializer_class = BirdSerializer


class BirdDetailView(View):

    def get(self, request, pks):
        queryset = Bird.objects.filter(pk__in=pks.split(','))

        data = {
            'birds': _get_map_data(queryset=queryset),
            'form_media': RangeForm().media,
        }
        return render(request, 'birds/details.html', data)


class BirdListView(View):

    def get(self, request):
        data = {
            'birds': _get_map_data(),
            'form_media': RangeForm().media,
        }
        return render(request, 'birds/bird_list.html', data)


def _get_map_data(queryset=None):
    world_borders = {
        border.name.lower(): border
        for border in WorldBorder.objects.all()
    }

    if all([query._meta.object_name == 'Bird' for query in queryset]):
        birds = queryset
    else:
        birds = (Bird.objects
                 .exclude(parsed_range='')
                 .exclude(common_name=''))
        birds = birds[:20]  # TODO: pagination

    bird_dicts = []
    for bird in birds:
        if bird.parsed_range != '':
            bird_regions = set(bird.parsed_range['region_atoms'])
        else:
            bird_regions = set()

        bird_dict = {
            'name': bird.common_name,
            'matched_regions': bird_regions & set(world_borders),
            'unmatched_regions': bird_regions - set(world_borders),
        }

        if bird_dict['matched_regions']:
            bird_world_borders = [
                world_borders[region_name]
                for region_name in bird_dict['matched_regions']]
            bird_dict['form'] = _get_range_form(bird, bird_world_borders)
        else:
            bird_dict['form'] = None

        bird_dicts.append(bird_dict)

    return bird_dicts


def _get_range_form(bird, world_borders):
    form_data = {
        'mpoly': reduce(operator.add, (border.mpoly
                                       for border in world_borders)),
    }
    return RangeForm(data=form_data,
                     auto_id='bird_%d_%%s' % bird.id)
