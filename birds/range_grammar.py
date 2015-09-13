# -*- coding: utf-8 -*-
import os
import re
from itertools import imap

from pyparsing import Keyword
from pyparsing import Group
from pyparsing import OneOrMore
from pyparsing import Optional
from pyparsing import Or
from pyparsing import Word
from pyparsing import Suppress
from pyparsing import ZeroOrMore
from pyparsing import alphas
from pyparsing import nums


def oneOfKeywords(iterable):
    return Or(imap(Keyword, iterable))


CHARACTERS = unicode(alphas) + u'ÉÎÑÓàáâãçèéêíïñóôõöúûüi'

REGIONS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'data',
    'regions.txt')


COMPASS_DIRECTION = oneOfKeywords(['north', 'east', 'south', 'west'])

# These should include 'n', 'sw', etc but that's not working currently and is
# handled by preprocess()
COMPASS_ADJECTIVE = oneOfKeywords([
    'central',
    'north', 'east', 'south', 'west',
    'northeast', 'northwest', 'southeast', 'southwest',
    'northern', 'eastern', 'southern', 'western',
    'northeastern', 'northwestern', 'southeastern', 'southwestern',

    # FIXME
    'northern and eastern', 'central and eastern', 'central and northeastern', 'central and southern', 'northern and central',
    'northwestern and north central',
    'southern-c', 'eastern-c',
    'north central', 'north-central', 'northern-central',
    'east central', 'east-central', 'eastern-central', 
    'south central', 'south-central', 'southern-central',
    'west central', 'west-central', 'western-central',
])
COMPASS_MODIFIER = oneOfKeywords([
    'adjacent',
    'extreme',
    'interior',
])
CONJUNCTION = Suppress(oneOfKeywords([
    ',',
    'and',
    ', and',
    ';',
]))
EXTINCTION_PHRASE = Or([
    (Keyword('extinct') + Optional(oneOfKeywords(['circa', 'ca']) + Word(nums))),
    (Keyword('extinct') + ';' + Keyword('last') + Keyword('reported') + Word(nums))
]) + Optional('.')


HABITAT_QUALIFIER = oneOfKeywords([
    'amazonian',
    'arctic',
    'arid',
    'coastal',
    'formerly',
    'immediately adjacent',    
    'locally in',
    'magellanic',
    'mainly in',
    'semiarid subtropical',
    'subtropical',
    'tropical',
    'patchily distributed',
])
VERB = oneOfKeywords([
    'breeds',
    'breeds from',
    'breeds in',
    'primarily winters in',
    'winters',
    'winters in',    
    'winters to',
])
FILL_OPERATOR = Optional(COMPASS_DIRECTION) + oneOfKeywords(['to'])
PARENTHETICAL_PHRASE = '(' + Word(CHARACTERS + ' ,?.-') + ')'
HABITAT = (
    Word(CHARACTERS) ^
    oneOfKeywords([
        u'alpine lakes',
        u'atlantic coast',
        u'andean foothills',
        u'aquatic lowlands',
        u'base of eastern andes',
        u'quebracho woodlands', # FIXME: "arid quebracho woodlands"
        u'caribbean slope',
        u'coast',
        u'desert puna',
        u'dry grasslands',
        u'dry savanna',
        u'gulf-caribbean lowlands',
        u'humid foothills',
        u'humid forests',
        u'humid lowlands',
        u'magdalena valley',
        u'maran valley',
        u'marañón valley',
        u'moist grasslands',
        u'moist chaco grasslands',
        u'montane forests',
        u'pacific and caribbean slopes',
        u'pacific lowlands',
        u'pacific slope',
        u'patagonian steppes',
        u'petén',
        u'semiarid grasslands',
        u'semiarid grasslands and scrub',
        u'taiga and wooded tundra',
        u'trans-fly savanna',
        u'tropical forests',
        # FIXME
        u'western slope of andes',
        u'wet lowlands',
    ])
) + oneOfKeywords([
    u'in',
    u'of',
])

IGNORED_WORDS = oneOfKeywords([
    'possibly',
])

def make_grammar():
    region_atom = oneOfKeywords(get_region_names(REGIONS_FILE))
    modified_compass_adjective = Optional(COMPASS_MODIFIER) + COMPASS_ADJECTIVE
    modified_region = Group(
        Optional(Group(Optional(modified_compass_adjective) + HABITAT)) + 
        Group(Optional(modified_compass_adjective) + region_atom)
    )
    region = Optional(VERB) + Group(modified_region + Optional(FILL_OPERATOR + modified_region))
    grammar = region + ZeroOrMore(Suppress(CONJUNCTION) + region) + Optional(Suppress('.'))

    grammar.ignore(PARENTHETICAL_PHRASE)

    grammar.ignore(EXTINCTION_PHRASE)

    # FIXME
    grammar.ignore(HABITAT_QUALIFIER)

    grammar.ignore(IGNORED_WORDS)
    
    return grammar


def preprocess(text):

    text = text.lower()

    # FIXME: use regexp
    text = (text
            .replace(' i. ', ' island ')
            .replace(' i.,', ' island,')
            .replace(' is. ', ' island ')
            .replace(' is.,', ' island,')
            .replace(' arch. ', ' archipelago ')
            .replace(' amaz. ', ' amazonian ')
            .replace(' ca. ', ' circa ')
    )

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
    ]:
        text = re.sub(pattern, replacement, text, flags=re.UNICODE)

    return text


def get_region_names(path):
    lines = []
    with open(path) as fp:
        for line in fp:
            if line.startswith('#'):
                continue
            line = line.strip()
            line = line.decode('utf8')
            # Strip inline comments
            line = re.sub(r'\s*#.*', '', line)
            lines.append(line)
    return lines


if __name__ == '__main__':

    from pprint import pprint

    from birds.models import Bird

    grammar = make_grammar()

    birds = (Bird.objects
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
            print grammar.parseString(text)
            print ex
            import ipdb ; ipdb.set_trace()
        else:
            pprint(parsed.asList(), width=30)

        print
        print '-' * 79
        print
            
