from pprint import pprint
import os

from pyparsing import Group
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
    'northern', 'eastern', 'southern', 'western',
    'northeastern', 'northwestern', 'southeastern', 'southwestern',
])
CONJUNCTION = oneOf([',', 'and', ', and'])
ADJECTIVE = oneOf(['coastal'])
FILL_OPERATOR = Optional(COMPASS_DIRECTION) + oneOf(['to'])
PARENTHETICAL_PHRASE = '(' + Word(alphas + ' ,') + ')'



def make_grammar():
    modified_region = Group(Optional(COMPASS_ADJECTIVE) + REGION_ATOM)
    region = Group(modified_region + Optional(FILL_OPERATOR + modified_region))
    grammar = region + ZeroOrMore(CONJUNCTION + region)
    grammar.ignore(PARENTHETICAL_PHRASE)
    grammar.ignore(ADJECTIVE)

    return grammar



def preprocess(text):
    return (
        text
        # These single/double letters seem to fail as compass adjectives
        # because they match incorrectly as prefixes of words.  Possibly need
        # to use Keyword instead of oneOf.
        .replace(' n ', ' northern ')
        .replace(' e ', ' eastern ')
        .replace(' s ', ' southern ')
        .replace(' w ', ' western ')
        .replace(' ne ', ' northwestern ')
        .replace(' se ', ' southeastern ')
        .replace(' sw ', ' southwestern ')
        .replace(' nw ', ' northwestern ')
    )


if __name__ == '__main__':
    range_texts = [
        "Senegambia to Ethiopia, n Uganda and ne Kenya",
        "Nigeria (east of Niger River) to Angola, Democratic Republic of the Congo, and Uganda",
        "Coastal n Australia and major offshore outlying islands",
        "India and Sri Lanka to se China, Indochina and Sumatra",
        "Nicobar Islands",
    ]
    grammar = make_grammar()
    for text in range_texts:
        text = preprocess(text)
        print text
        try:
            pprint(grammar.parseString(text.lower()).asList(), width=30)
        except Exception as ex:
            print ex
            import ipdb ; ipdb.set_trace()
        print
        print '-' * 79
        print
