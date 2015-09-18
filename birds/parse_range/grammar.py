# -*- coding: utf-8 -*-
import re

from pyparsing import And
from pyparsing import Group
from pyparsing import Keyword
from pyparsing import OneOrMore
from pyparsing import Optional
from pyparsing import Or
from pyparsing import Suppress
from pyparsing import Word
from pyparsing import ZeroOrMore
from pyparsing import alphas
from pyparsing import nums
from pyparsing import oneOf
from pyparsing import CharsNotIn

from birds.parse_range.utils import one_of_keywords
from birds.parse_range.utils import one_of_keywords_in_file
from birds.parse_range.utils import one_of_phrases
from birds.parse_range.utils import one_of_phrases_in_file


CHARACTERS = unicode(alphas) + u'ÉÎÑÓàáâãçèéêíïñóôõöúûüi'

REGION_ATOM = one_of_keywords_in_file('regions.txt')

# These should include 'n', 'sw', etc but that's not working currently and is
# handled by preprocess()
COMPASS_DIRECTION = one_of_keywords([
    u'north',
    u'east',
    u'south',
    u'west',
])

COMPASS_ADJECTIVE = one_of_keywords_in_file('compass_adjectives.txt')

REGION_MODIFIER = one_of_phrases([
    u'adjacent',
    u'alpine',
    u'arctic',
    u'arid',
    u'borders of',
    u'coastal',
    u'east slope of',  # FIXME
    u'eastern arctic',  # FIXME
    u'eastern slope of',  # FIXME
    u'equatorial',
    u'extreme north coastal',  # FIXME
    u'extreme',
    u'humid',
    u'immediately adjacent',
    u'interior',
    u'lowland',
    u'magellanic',
    u'montane',
    u'north central arctic',  # FIXME
    u'northeastern arctic',  # FIXME
    u'northern half of',
    u'northwestern arctic',  # FIXME
    u'semiarid subtropical',
    u'semiarid',
    u'subtropical',
    u'temperate',
    u'tropical',
    u'west equatorial',  # FIXME
    u'west slope of',  # FIXME
    u'western slope of',  # FIXME
    u'mid-montane',
    u'south slopes of',
    u'low altitude',
])

OCURRENCE_MODIFIER = one_of_phrases([
    u'discontinuous',
    u'formerly',
    u'locally in',
    u'local in',
    u'locally on',
    u'locally from',
    u'mainly in',
    u'nomadic throughout',
    u'patchily distributed',
    u'patchily distributed in',
    u'widespread',
    u'mainly',
    u'discontinuous in',
])

HABITAT = one_of_keywords_in_file('habitats.txt')

HABITAT_PREPOSITION = one_of_keywords([
    u'in',
    u'of',
    u'off',
    u'off of',
    u'from',
])

VERB = one_of_keywords([
    u'breeds',
    u'breeds from',
    u'breeds in',
    u'migrates',
    u'migrates north to',
    u'resident',
    u'primarily winters in',
    u'winters primarily in',
    u'winters',
    u'winters in',
    u'winters to',
    u'winters north to',
    u'winters south to',
    u'winters on',
    u'introduced to',
    u'visitor to',
])

FILL_OPERATOR = Optional(COMPASS_DIRECTION) + one_of_keywords(['to', 'through'])

CONJUNCTION = Suppress(one_of_keywords([
    u',',
    u'and',
    u', and',
    u', and to',  # FIXME
    u'and in the',
    u';',
    u', also on',
    u', and south to',  # FIXME
]))

PARENTHETICAL_PHRASE = (
    '(' +
    Word(CHARACTERS + unicode(nums) + u' ,?.-:±/') +
    ')'
)

COLON_PHRASE = ':' + CharsNotIn('.;') + Optional(oneOf(['.', ';']))

IGNORED_PHRASES = Or([
    one_of_phrases_in_file('ignored_phrases.txt'),
    (Keyword(u'extinct') + Optional(one_of_keywords([u'circa', u'ca']) + Word(nums))),
    (Keyword(u'extinct') + u';' + Keyword(u'last') + Keyword(u'reported') + Word(nums)),
])

IGNORED_WORDS = one_of_keywords([
    u'the',
    u'possibly',
])

def make_grammar():
    compound_compass_adjective = (
        COMPASS_ADJECTIVE +
        Optional(Optional(Or(['-', 'and'])) + COMPASS_ADJECTIVE)
    )
    modifier = ZeroOrMore(REGION_MODIFIER) + Optional(compound_compass_adjective)
    modified_region = Group(Or([
        (Optional(Group(Optional(modifier) + HABITAT + HABITAT_PREPOSITION)) +
         Group(Optional(modifier) + REGION_ATOM)),
        (Optional(HABITAT) + COMPASS_DIRECTION + 'of' + REGION_ATOM),
    ]))
    region = Group(
        Optional(VERB) +
        Optional(Keyword('from')) +
        modified_region +
        Optional(Optional(Keyword('from') + modified_region) +
                 OneOrMore(Group(FILL_OPERATOR + modified_region)))
    )
    grammar = region + ZeroOrMore(Suppress(CONJUNCTION) + region) + Optional(Suppress('.'))

    grammar.ignore(OCURRENCE_MODIFIER)

    grammar.ignore(Optional(oneOf([u';', u',', u'.'])) + IGNORED_PHRASES + Optional(u'.'))
    grammar.ignore(IGNORED_WORDS)
    grammar.ignore(PARENTHETICAL_PHRASE)
    grammar.ignore(COLON_PHRASE)

    return grammar


def preprocess(text):

    text = text.lower()

    # FIXME: use regexp
    text = (text
            .replace(' i.', ' island')
            .replace(' i.,', ' island,')
            .replace(' is.', ' island')
            .replace(' mts.', ' mountains')
            .replace(' arch.', ' archipelago')
            .replace(' amaz. ', ' amazonian ')
            .replace(' ca. ', ' circa ')
            .replace(' pen.', ' peninsula')
            .replace(' r.', ' river')
    )

    text = (text
            .replace('black, caspian and aral seas',
                     'black sea, caspian sea and aral sea')
            .replace('north, south and stewart islands',
                     'north island, south island and stewart island')
            .replace('misool and salawati islands',
                     'misool island and salawati island')
            .replace('bangka, lembeh and butung islands',
                     'bangka island, lembeh island and butung island')
            .replace('sangihe, siau, tahulandang and ruang islands',
                     'sangihe island, siau island, tahulandang island and ruang island')
            .replace('banggai and sula islands',
                     'banggai island and sula island')
            .replace('banka and belitung islands',
                     'banka island and belitung island')
            .replace('kofiau, kamuai, and misool island',
                     'kofiau island, kamuai island and misool island')
            .replace('eastern-c',
                     'eastern-central')
            .replace('southern-c',
                     'southern-central')
            .replace('talisei, tendila, lembeh and togian islands',
                     'talisei island, tendila island, lembeh island and togian islands')
            .replace('temp. e andes',
                     'temperate e andes')
    )

    # These single/double letters seem to fail as compass adjectives
    # because they match incorrectly as prefixes of words.  Possibly need
    # to use Keyword instead of oneOf.
    # FIXME: This is incorrect for e.g. the country "S Africa"
    for pattern, replacement in [
            (r'\bn\b', 'north'),
            (r'\be\b', 'east'),
            (r'\bs\b', 'south'),
            (r'\bw\b', 'west'),
            (r'\bc\b', 'central'),
            (r'\bne\b', 'northeastern'),
            (r'\bse\b', 'southeastern'),
            (r'\bsw\b', 'southwestern'),
            (r'\bnw\b', 'northwestern'),
            (r'^mts\. ', 'mountains '),
            # Force punctuation to be word-end by adding space, so that Keyword
            # can be used rather than Literal
            # FIXME: can this be avoided?
            (r'\b([,;.])', ' \\1'),
            (r'(\))([,;.])', '\\1 \\2'),
            # Remove comma before fill operator
            (r', (north|east|south|west) to', ' \\1 to'),
    ]:
        text = re.sub(pattern, replacement, text, flags=re.UNICODE)

    return text


if __name__ == '__main__':
    import sys

    args = sys.argv[1:]
    if args:
        # Optional primary key to start at
        [offset] = args
        offset = int(offset)
    else:
        offset = None

    from pprint import pprint

    from birds.models import Bird

    grammar = make_grammar()

    unparseable = [109, 327, 361, 375, 529, 536, 587, 606, 631, 978, 1071]

    birds = (Bird.objects
             .exclude(id__in=unparseable)
             .order_by('id'))

    if offset:
        birds = birds.filter(id__gte=offset)

    for bird in birds:
        if not bird.raw_range:
            continue

        print bird.id, bird.order, bird.family, bird.genus, bird.species, bird.subspecies, bird.common_name
        print

        text = preprocess(bird.raw_range)
        print text
        print

        try:
            parsed = grammar.parseString(text, parseAll=True)
        except Exception as ex:
            try:
                pprint(grammar.parseString(text).asList(), width=30)
            except:
                print '[cannot partially parse]'
            print ex
            import ipdb ; ipdb.set_trace()
        else:
            pprint(parsed.asList(), width=30)

        print
        print '-' * 79
        print
