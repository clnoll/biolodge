from pprint import pprint
import pickle
import sys

from django.core.management.base import BaseCommand

from pyparsing import ParseException

from birds.models import Bird
from birds.parse_range.grammar import make_range_grammar
from birds.parse_range.grammar import preprocess


PARSE_RANGE_FAILURE_STRING = '<FAILED_TO_PARSE_RANGE>'


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
                 .exclude(parsed_range=PARSE_RANGE_FAILURE_STRING)
                 .order_by('id')
                 .filter(parsed_range=''))

        if options['offset']:
            birds = birds.filter(id__gte=options['offset'])

        n_birds = birds.count()

        for i, bird in enumerate(birds):

            if not bird.raw_range:
                continue

            print ' '.join(['%d/%d' % (i, n_birds),
                            str(bird.id),
                            bird.order,
                            bird.family,
                            bird.genus,
                            bird.species,
                            bird.subspecies,
                            bird.common_name])
            print

            text = preprocess(bird.raw_range)
            print text
            print

            try:
                parsed = grammar.parseString(text, parseAll=True).asList()
            except ParseException as ex:
                print >>sys.stderr, '%s: %s' % (type(ex).__name__, ex)
                parsed = PARSE_RANGE_FAILURE_STRING

            bird.parsed_range = pickle.dumps(parsed)
            bird.save()

            pprint(parsed)
            print
            print '-' * 79
            print
