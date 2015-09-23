from django.shortcuts import render
from django.views.generic import View

from birds.models import Bird
from geo.models import WorldBorder


class MapView(View):

    def get(self, request):
        # import ipdb; ipdb.set_trace()

        borders = set(WorldBorder.objects.values_list('name', flat=True))

        species_with_known_range = Bird.objects.exclude(parsed_range='')

        species_with_known_range = species_with_known_range[:20]

        data = {
            'birds': {},
        }

        birds = data['birds']

        for species in species_with_known_range:
            name = species.common_name
            birds[name] = {}
            birds[name]['matched_species_polys'] = []
            birds[name]['unmatched_species_polys'] = []

            species_regions = species.parsed_range['region_atoms']
            for region in species_regions:
                if region in borders:
                    birds[name]['matched_species_polys'].append(region)
                else:
                    birds[name]['unmatched_species_polys'].append(region)

        return render(request, 'geo/geo.html', data)
