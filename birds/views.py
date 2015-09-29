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
        world_borders = {
            border.name.lower(): border
            for border in WorldBorder.objects.all()
        }

        queryset = Bird.objects.filter(pk__in=pks.split(','))
        birds = _get_map_data(queryset=queryset)

        concat_birds = {'names': [],
                        'ids': '',
                        'matched_regions': set([]),
                        'unmatched_regions': set([]),
                        'form': '',
                        }

        for bird in birds:
            concat_birds['names'].append(bird['name'])
            concat_birds['ids'] = '%s_%s' % (concat_birds['ids'], bird['_id'])
            concat_birds['matched_regions'] = concat_birds['matched_regions'] | bird['matched_regions']
            concat_birds['unmatched_regions'] = concat_birds['unmatched_regions'] | bird['unmatched_regions']

        if concat_birds['matched_regions']:
            bird_world_borders = [
                world_borders[region_name]
                for region_name in concat_birds['matched_regions']]
            concat_birds['form'] = _get_range_form(concat_birds, bird_world_borders, concat=True)
        else:
            concat_birds['form'] = None

        from django.contrib.gis.serializers import geojson
        serializer = geojson.Serializer()
        world_borders_json = serializer.serialize(bird_world_borders)

        with open('/Users/dan/tmp/geojson/countries.json') as fp:
            world_borders_json = fp.read()

        data = {
            'birds': concat_birds,
            'form_media': RangeForm().media,
            'world_borders_json': world_borders_json,
        }
        return render(request, 'birds/details.html', data)


class BirdListView(View):

    PAGE_SIZE = 10

    def get(self, request):
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

        bird_dicts = _get_map_data()

        data = {
            'birds': bird_dicts,
            'form_media': RangeForm().media,
            'previous_page': previous_page,
            'next_page': next_page,
        }

        return render(request, 'birds/bird_list.html', data)


def _get_map_data(queryset=None):
    world_borders = {
        border.name.lower(): border
        for border in WorldBorder.objects.all()
    }

    if queryset:
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
            '_id': bird.id,
            'name': bird.common_name,
            'genus': bird.genus,
            'species': bird.species,
            'subspecies': bird.subspecies,
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

    return bird_dicts


def _get_range_form(bird, world_borders, concat=False):
        form_data = {
            'mpoly': reduce(operator.add, (border.mpoly
                                           for border in world_borders)),
        }
        if concat:
            return RangeForm(data=form_data,
                             auto_id='bird_%s_%%s' % bird['ids'])
        return RangeForm(data=form_data,
                         auto_id='bird_%d_%%s' % bird.id)
