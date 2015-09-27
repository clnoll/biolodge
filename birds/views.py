import operator

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from rest_framework import generics
from rest_framework.serializers import ModelSerializer

from birds.forms import RangeForm
from birds.forms import FilterForm
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
    queryset = (Bird.objects
                .all()
                .exclude(parsed_range='')
                .exclude(common_name=''))

    def get(self, request, queryset=None):
        world_borders = {
            border.name.lower(): border
            for border in WorldBorder.objects.all()
        }

        birds = queryset or self.queryset

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

        data = {
            'birds': bird_dicts,
            'map_widget_media': RangeForm().media,
            'previous_page': previous_page,
            'next_page': next_page,
            'filter_form': FilterForm(),
        }

        return render(request, 'birds/bird_list.html', data)


def _get_range_form(bird, world_borders):
    form_data = {
        'mpoly': reduce(operator.add, (border.mpoly
                                       for border in world_borders)),
    }
    return RangeForm(data=form_data,
                     auto_id='bird_%d_%%s' % bird.id)


class BirdListFilter(View):

    def post(self, request):
        name_query = self.get_name_query(request.POST['name'])
        range_query = self.get_range_query(request.POST['range'])
        queryset = BirdListView.queryset.filter(name_query & range_query)
        return BirdListView().get(request, queryset=queryset)

    def get_name_query(self, string):
        query = Q()
        string = string.strip()
        for word in string.split():
            query |= Q(common_name__icontains=word)
            query |= Q(genus__icontains=word)
            query |= Q(species__icontains=word)
            query |= Q(subspecies__icontains=word)
        return query

    def get_range_query(self, string):
        query = Q()
        string = string.strip()
        if string:
            return Q(raw_range__icontains=string)
        else:
            return Q()
