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
    'northern and eastern', 'central and eastern', 'central and northeastern', 'central and southern', 'northern and central',
    'southern-c', 'eastern-c',
    'south central', 'north-central', 'northern-central', 'southern-central', 'eastern-central', 'western-central', 'east central',
])
COMPASS_MODIFIER = oneOf(['extreme', 'interior'])
CONJUNCTION = oneOf([
    ',',
    'and',
    ', and',
])
HABITAT_QUALIFIER = oneOf([
    'amazonian',
    'arid',
    'coastal',
    'formerly',
    'locally in',
    'mainly in',
    'semiarid subtropical',
    'subtropical',
    'tropical',
    'patchily distributed',
])
VERB = oneOf([
    'breeds',
    'winters',
])
FILL_OPERATOR = Optional(COMPASS_DIRECTION) + oneOf(['to'])
PARENTHETICAL_PHRASE = '(' + Word(alphas + ' ,') + ')'
HABITAT = (
    Word(alphas)
    ^ 'atlantic coast'
    ^ 'andean foothills'
    ^ 'aquatic lowlands'
    # FIXME: "arid quebracho woodlands"
    ^ 'quebracho woodlands'
    ^ 'caribbean slope'
    ^ 'coast'
    ^ 'desert puna'
    ^ 'dry grasslands'
    ^ 'dry savanna'
    ^ 'gulf-caribbean lowlands'
    ^ 'humid foothills'
    ^ 'humid forests'
    ^ 'humid lowlands'
    ^ 'magdalena valley'
    ^ 'maran valley'
    ^ 'moist grasslands'
    ^ 'moist chaco grasslands'
    ^ 'montane forests'
    ^ 'pacific and caribbean slopes'
    ^ 'pacific lowlands'
    ^ 'pacific slope'
    ^ 'patagonian steppes'
    ^ 'semiarid grasslands'
    ^ 'semiarid grasslands and scrub'
    ^ 'taiga and wooded tundra'
    ^ 'tropical forests'
    # FIXME
    ^ 'western coast of greenland'
    # FIXME
    ^ 'western slope of andes'
    ^ 'wet lowlands'
) + oneOf(['in', 'of'])


def make_grammar():

    modified_region = Group(Optional(HABITAT) +
                            Optional(Optional(COMPASS_MODIFIER) + COMPASS_ADJECTIVE) +
                            REGION_ATOM)
    region = Optional(VERB) + Group(modified_region + Optional(FILL_OPERATOR + modified_region))
    grammar = region + ZeroOrMore(CONJUNCTION + region)
    grammar.ignore(PARENTHETICAL_PHRASE)

    # FIXME
    grammar.ignore(HABITAT_QUALIFIER)

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

    # FIXME: use regexp
    text = (text
            .replace(' i. ', ' island ')
            .replace(' i.,', ' island,')
            .replace(' arch. ', ' archipelago '))

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
