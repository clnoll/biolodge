import pickle

from django.core.management.base import BaseCommand

from birds.models import Bird
from birds.parse_range.grammar import compute_range


class Command(BaseCommand):
    help = 'Compute MultiPolygons from parsed range ASTs'

    def handle(self, *args, **options):
        birds = (Bird.objects
                 .exclude(parsed_range='')
                 .order_by('id'))

        for bird in birds:
            print bird.id
            parsed_range = pickle.loads(bird.parsed_range)
            bird.mpoly = compute_range(parsed_range)
            bird.save()
