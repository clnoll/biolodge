import os
from functools import partial

from django.core.management.base import BaseCommand

from birds import parse_range
from birds.models import Bird
from birds.parse_range.utils import read_lines


REGIONS_FILE = os.path.join(os.path.dirname(parse_range.__file__),
                            'regions.txt')


class Command(BaseCommand):
    help = 'List regions from raw range fields'

    def handle(self, *args, **options):
        with open(REGIONS_FILE) as fp:
            regions = list(read_lines(fp))
        ranges = Bird.objects.values_list('raw_range', flat=True)
        ranges = set(s.lower() for s in ranges)
        regions = filter(partial(search, strings=ranges), regions)
        for region in regions:
            print region.encode('utf-8')


def search(substring, strings):
    for string in strings:
        if substring in string:
            return True
    return False
