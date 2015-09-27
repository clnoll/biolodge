import operator

from django.shortcuts import render
from django.views.generic import View

from birds.forms import RangeForm
from birds.models import Bird
from geo.models import WorldBorder


class MapView(View):

    def get(self, request):
        world_borders = {
            border.name.lower(): border
            for border in WorldBorder.objects.all()
        }

        species_with_known_range = (Bird.objects
                                    .exclude(parsed_range='')
                                    .exclude(common_name=''))

        species_with_known_range = species_with_known_range[:20]  # TODO: pagination

        data = {
            'birds': {},
            'form_media': RangeForm().media,
        }

        birds = data['birds']

        for species in species_with_known_range:
            name = species.common_name
            species_regions = set(species.parsed_range['region_atoms'])
            species_data = {}

            species_data['matched_species_regions'] = (
                species_regions & set(world_borders))
            species_data['unmatched_species_regions'] = (
                species_regions - species_data['matched_species_regions'])

            if species_data['matched_species_regions']:
                region_names = species_data['matched_species_regions']

                mpoly = reduce(
                    operator.add,
                    [world_borders[region_name].mpoly
                     for region_name in region_names])

                form_data = {
                    'name': name,
                    'mpoly': mpoly,
                }
                species_data['form'] = RangeForm(
                    data=form_data,
                    auto_id='bird_%d_%%s' % species.id)
            else:
                species_data['form'] = None

            birds[name] = species_data

        return render(request, 'geo/geo.html', data)
