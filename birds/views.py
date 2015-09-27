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


class BirdListView(View):
    PAGE_SIZE = 10

    def get(self, request):
        world_borders = {
            border.name.lower(): border
            for border in WorldBorder.objects.all()
        }

        birds = (Bird.objects
                 .exclude(parsed_range='')
                 .exclude(common_name=''))

        # Calculate pagination
        page = int(request.GET.get('page', '1'))
        birds_last_index = birds.count() - 1
        page_first_index = (page - 1) * self.PAGE_SIZE
        page_last_index = min(page * self.PAGE_SIZE - 1,
                              birds_last_index)
        previous_page = page - 1 if page > 1 else None
        next_page = page + 1 if birds_last_index > page_last_index else None
        birds = birds[page_first_index:page_last_index + 1]

        bird_dicts = []
        for bird in birds:
            bird_regions = set(bird.parsed_range['region_atoms'])

            bird_dict = {
                'name': bird.common_name,
                'raw_range': bird.raw_range,
                'parsed_range': bird.parsed_range,
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

        data = {
            'birds': bird_dicts,
            'form_media': RangeForm().media,
            'previous_page': previous_page,
            'next_page': next_page,
        }

        return render(request, 'birds/bird_list.html', data)


def _get_range_form(bird, world_borders):
    form_data = {
        'mpoly': reduce(operator.add, (border.mpoly
                                       for border in world_borders)),
    }
    return RangeForm(data=form_data,
                     auto_id='bird_%d_%%s' % bird.id)
