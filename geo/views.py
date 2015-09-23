from django.shortcuts import render
from django.views.generic import View

from birds.forms import RangeForm
from birds.models import Bird
from geo.models import WorldBorder


class MapView(View):

    def get(self, request):
        borders = set(s.lower() for s in WorldBorder.objects.values_list('name', flat=True))

        species_with_known_range = (Bird.objects
                                    .exclude(parsed_range='')
                                    .exclude(common_name=''))

        species_with_known_range = species_with_known_range[:20]

        data = {
            'birds': {},
            'form_media': RangeForm().media,
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
                    region = WorldBorder.objects.get(name__iexact=region)
                else:
                    birds[name]['unmatched_species_polys'].append(region)

            if birds[name]['matched_species_polys']:
                region_names = birds[name]['matched_species_polys']
                mpoly = WorldBorder.objects.get(name__iexact=region_names[0]).mpoly
                for region_name in region_names[1:]:
                    mpoly += WorldBorder.objects.get(name__iexact=region_name).mpoly
                form = RangeForm(data={
                    'name': name,
                    'mpoly': mpoly,
                })
                birds[name]['form'] = form
            else:
                birds[name]['form'] = None

            print 'Created entry: name=%s, form=%s,%s, #regions=%d' % (
                name,
                bool(form),
                id(form),
                len(birds[name]['matched_species_polys']),
            )


        return render(request, 'geo/geo.html', data)
