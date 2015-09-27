from birds.forms import RangeForm
from birds.models import Bird
from geo.models import WorldBorder


def get_map_data_from_birds(birds=None):

        world_borders = {
            border.name.lower(): border
            for border in WorldBorder.objects.all()
        }


# def get_map_data_from_regions(regions=None):
#     pass
