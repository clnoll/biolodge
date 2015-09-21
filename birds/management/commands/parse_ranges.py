from pprint import pprint

from django.core.management.base import BaseCommand

from birds.models import Bird
from birds.parse_range.grammar import make_range_grammar
from birds.parse_range.grammar import preprocess


class Command(BaseCommand):
    help = 'Parse raw range fields'

    def add_arguments(self, command_parser):
        command_parser.add_argument('offset', nargs='?', type=int,
                                    help="Optional primary key to start at")

    def handle(self, *args, **options):
        grammar = make_range_grammar()
        unparseable = [109, 327, 361, 375, 529, 536, 587, 606, 631, 978, 1071]

        birds = (Bird.objects
                 .exclude(id__in=unparseable)
                 .order_by('id'))

        if options['offset']:
            birds = birds.filter(id__gte=options['offset'])

        for bird in birds:
            if not bird.raw_range:
                continue

            print(bird.id,
                  bird.order,
                  bird.family,
                  bird.genus,
                  bird.species,
                  bird.subspecies,
                  bird.common_name)
            print

            text = preprocess(bird.raw_range)
            print text
            print

            try:
                parsed = grammar.parseString(text, parseAll=True)
            except Exception as ex:
                import ipdb ; ipdb.set_trace()
            else:
                pprint(parsed.asList(), width=30)

            print
            print '-' * 79
            print
