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
    u'formerly',
    u'immediately adjacent',    
    u'locally in',
    u'magellanic',
    u'mainly in',
    u'semiarid subtropical',
    u'subtropical',
    u'tropical',
    u'patchily distributed',
])
VERB = oneOfKeywords([
    u'breeds',
    u'breeds from',
    u'breeds in',
    u'migrates',
    u'migrates north to',
    u'resident',
    u'primarily winters in',
    u'winters',
    u'winters in',    
    u'winters to',
    u'winters on',
    u'introduced to',
])
FILL_OPERATOR = Optional(COMPASS_DIRECTION) + oneOfKeywords(['to'])
PARENTHETICAL_PHRASE = '(' + Word(CHARACTERS + ' ,?.-:') + ')'
HABITAT = (Word(CHARACTERS) ^ oneOfKeywordsInFile('habitats.txt')) + oneOfKeywords([
    u'in',
    u'of',
])

IGNORED_WORDS = oneOfKeywords([
    u'possibly',
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
                 FILL_OPERATOR +
                 modified_region)
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
            .replace(' i. ', ' island ')
            .replace(' i.,', ' island,')
            .replace(' is.', ' island')
            .replace(' arch. ', ' archipelago ')
            .replace(' amaz. ', ' amazonian ')
            .replace(' ca. ', ' circa ')
    )

    text = (text
            .replace('black, caspian and aral seas',
                     'black sea, caspian sea and aral sea')
            .replace('north, south and stewart islands',
                     'north island, south island and stewart island'))
    
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

    from pprint import pprint

    from birds.models import Bird

    grammar = make_grammar()

    birds = (Bird.objects
             .filter(id__gte=364)
             .order_by('id'))
    
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
            import ipdb ; ipdb.set_trace()
        else:
            pprint(parsed.asList(), width=30)

        print
        print '-' * 79
        print
            
