import os
import re

from pyparsing import Group
from pyparsing import OneOrMore
from pyparsing import Optional
from pyparsing import Word
from pyparsing import ZeroOrMore
from pyparsing import alphas
from pyparsing import oneOf


REGIONS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'data',
    'regions.txt')

with open(REGIONS_FILE) as fp:
    REGION_ATOM = oneOf(line.strip() for line in fp
                        if not line.startswith('#'))

COMPASS_DIRECTION = oneOf(['north', 'east', 'south', 'west'])

# These should include 'n', 'sw', etc but that's not working currently and is
# handled by preprocess()
COMPASS_ADJECTIVE = oneOf([
    'central',
    'north', 'east', 'south', 'west',
    'northern', 'eastern', 'southern', 'western',
    'northeastern', 'northwestern', 'southeastern', 'southwestern',

    # FIXME
    'northern and eastern', 'central and eastern',
    'southern-c', 'northern-central', 'southern-central',
])
COMPASS_MODIFIER = oneOf(['extreme'])
CONJUNCTION = oneOf([',', 'and', ', and'])
ADJECTIVE = oneOf(['amazonian', 'coastal', 'formerly', 'subtropical', 'tropical'])
FILL_OPERATOR = Optional(COMPASS_DIRECTION) + oneOf(['to'])
PARENTHETICAL_PHRASE = '(' + Word(alphas + ' ,') + ')'
HABITAT = (Word(alphas)
           ^ 'desert puna'
           ^ 'patagonian steppes'
           ^ 'montane forests'
           ^ 'pacific slope'
           ^ 'humid lowlands'
           ^ 'pacific and caribbean slopes'
           ^ 'magdalena valley') + 'of'


def make_grammar():
    modified_region = Group(Optional(HABITAT) +
                            Optional(Optional(COMPASS_MODIFIER) + COMPASS_ADJECTIVE) +
                            REGION_ATOM)
    region = Group(modified_region + Optional(FILL_OPERATOR + modified_region))
    grammar = region + ZeroOrMore(CONJUNCTION + region)
    grammar.ignore(PARENTHETICAL_PHRASE)

    # FIXME
    grammar.ignore(ADJECTIVE)

    return grammar



def preprocess(text):

    text = text.lower()

    # These single/double letters seem to fail as compass adjectives
    # because they match incorrectly as prefixes of words.  Possibly need
    # to use Keyword instead of oneOf.
    # FIXME: This is incorrect for e.g. the country "S Africa"
    for pattern, replacement in [
            (r'\bn\b', 'northern'),
            (r'\be\b', 'eastern'),
            (r'\bs\b', 'southern'),
            (r'\bw\b', 'western'),
            (r'\bne\b', 'northeastern'),
            (r'\bse\b', 'southeastern'),
            (r'\bsw\b', 'southwestern'),
            (r'\bnw\b', 'northwestern'),
    ]:
        text = re.sub(pattern, replacement, text)

    return text


if __name__ == '__main__':

    from pprint import pprint

    from birds.models import Bird

    grammar = make_grammar()
    for bird in Bird.objects.order_by('id'):
        if not bird.raw_range:
            continue

        text = preprocess(bird.raw_range)
        print bird.id
        print text
        try:
            pprint(grammar.parseString(text.lower()).asList(), width=30)
        except Exception as ex:
            print ex
            import ipdb ; ipdb.set_trace()
        print
        print '-' * 79
        print
