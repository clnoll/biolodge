# -*- coding: utf-8 -*-
import re

from pyparsing import Keyword
from pyparsing import Group
from pyparsing import OneOrMore
from pyparsing import Optional
from pyparsing import Or
from pyparsing import And
from pyparsing import Word
from pyparsing import Suppress
from pyparsing import ZeroOrMore
from pyparsing import oneOf
from pyparsing import alphas
from pyparsing import nums

from birds.parse_range.utils import oneOfKeywords
from birds.parse_range.utils import oneOfKeywordsInFile
from birds.parse_range.utils import Phrase


CHARACTERS = unicode(alphas) + u'ÉÎÑÓàáâãçèéêíïñóôõöúûüi'

REGION_ATOM = oneOfKeywordsInFile('regions.txt')

# These should include 'n', 'sw', etc but that's not working currently and is
# handled by preprocess()
COMPASS_DIRECTION = oneOfKeywords([u'north', u'east', u'south', u'west'])
COMPASS_ADJECTIVE = oneOfKeywordsInFile('compass_adjectives.txt')

COMPASS_MODIFIER = oneOfKeywords([
    u'adjacent',
    u'extreme',
    u'interior',
    u'equatorial',
])
CONJUNCTION = Suppress(oneOfKeywords([
    u',',
    u'and',
    u', and',
    u', and to',  # FIXME
    u';',
]))

HABITAT_QUALIFIER = oneOfKeywords([
    u'amazonian',
    u'arctic',
    u'arid',
    u'coastal',
    u'discontinuous',
    u'formerly',
    u'immediately adjacent',
    u'interior',
    u'locally in',
    u'locally on',
    u'locally from',
    u'magellanic',
    u'mainly in',
    u'nomadic throughout',
    u'semiarid subtropical',
    u'subtropical',
    u'tropical',
    u'patchily distributed',
    u'widespread',
    u'western slope of',
    u'northern half of',
])
VERB = oneOfKeywords([
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
FILL_OPERATOR = Optional(COMPASS_DIRECTION) + oneOfKeywords(['to'])
PARENTHETICAL_PHRASE = '(' + Word(CHARACTERS + unicode(nums) + u' ,?.-:±') + ')'
HABITAT = oneOfKeywordsInFile('habitats.txt') + oneOfKeywords([
    u'in',
    u'of',
    u'off',
])

IGNORED_WORDS = oneOfKeywords([
    u'possibly',
    u'mainly',
    u'the',
])

IGNORED_PHRASES = Or([
    (Keyword(u'extinct') + Optional(oneOfKeywords([u'circa', u'ca']) + Word(nums))),
    (Keyword(u'extinct') + u';' + Keyword(u'last') + Keyword(u'reported') + Word(nums)),
    Phrase(u'southward in winter'),
    Phrase(u'introduced widely'),
    Phrase(u'now only on wildlife reserves'),
    Phrase(u'primarily resident'),
    Phrase(u'where formerly occurred but was eradicated'),
    Phrase(u'later was re-introduced and also self-colonized'),
    Phrase(u'on verge of extinction'),
    Phrase(u'just south of the central mountain ranges'),
])


def make_grammar():
    modified_compass_adjective = Optional(COMPASS_MODIFIER) + Optional(COMPASS_ADJECTIVE)
    modified_region = Group(
        Optional(Group(Optional(modified_compass_adjective) + HABITAT)) +
        Group(Optional(modified_compass_adjective) + REGION_ATOM)
    )
    region = Group(
        Optional(VERB) +
        Optional(Keyword('from')) +
        modified_region +
        Optional(Optional(Keyword('from') + modified_region) +
                 OneOrMore(Group(FILL_OPERATOR + modified_region)))
    )
    grammar = region + ZeroOrMore(Suppress(CONJUNCTION) + region) + Optional(Suppress('.'))

    grammar.ignore(PARENTHETICAL_PHRASE)

    # FIXME
    grammar.ignore(HABITAT_QUALIFIER)

    grammar.ignore(IGNORED_WORDS)
    grammar.ignore(Optional(oneOf([u';', u','])) + IGNORED_PHRASES + Optional(u'.'))


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
    )

    text = (text
            .replace('black, caspian and aral seas',
                     'black sea, caspian sea and aral sea')
            .replace('north, south and stewart islands',
                     'north island, south island and stewart island')
            .replace('misool and salawati islands',
                     'misool island and salawati island')
            .replace('bangka, lembeh and butung islands',
                     'bangka island, lembeh island and butung island'))

    # These single/double letters seem to fail as compass adjectives
    # because they match incorrectly as prefixes of words.  Possibly need
    # to use Keyword instead of oneOf.
    # FIXME: This is incorrect for e.g. the country "S Africa"
    for pattern, replacement in [
            (r'\bn\b', 'northern'),
            (r'\be\b', 'eastern'),
            (r'\bs\b', 'southern'),
            (r'\bw\b', 'western'),
            (r'\bc\b', 'central'),
            (r'\bne\b', 'northeastern'),
            (r'\bse\b', 'southeastern'),
            (r'\bsw\b', 'southwestern'),
            (r'\bnw\b', 'northwestern'),
            # Force punctuation to be word-end by adding space, so that Keyword
            # can be used rather than Literal
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

    from pprint import pprint

    from birds.models import Bird

    grammar = make_grammar()

    unparseable = [375, 529, 536, 587, 606, 631]

    birds = (Bird.objects
             .exclude(id__in=unparseable)
             .order_by('id'))

    if offset:
        birds = birds.filter(id__gte=offset)

    for bird in birds:
        if not bird.raw_range:
            continue

        print bird.id

        text = preprocess(bird.raw_range)
        print text

        # parsed = grammar.parseString(text, parseAll=True)

        try:
            parsed = grammar.parseString(text, parseAll=True)
        except Exception as ex:
            pprint(grammar.parseString(text).asList(), width=30)
            print ex
        else:
            pprint(parsed.asList(), width=30)

        print
        print '-' * 79
        print
