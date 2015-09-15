import os
import re
from itertools import ifilter
from itertools import imap

from pyparsing import Keyword
from pyparsing import And
from pyparsing import Or


def Phrase(string):
    return And(map(Keyword, string.split()))


def oneOfKeywords(strings):
    return _oneOfStrings(strings, Keyword)


def oneOfKeywordsInFile(path):
    return _oneOfStringsInFile(path, Keyword)


def oneOfPhrasesInFile(path):
    return _oneOfStringsInFile(path, Phrase)


def _oneOfStringsInFile(path, cls):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        path)
    with open(path) as fp:
        lines = ifilter(None, imap(process_line, fp))
        return _oneOfStrings(lines, cls)


def _oneOfStrings(strings, cls):
    return Or(imap(cls, strings))


def process_line(line):
    line = line.strip()
    line = line.decode('utf8')
    # Strip inline comments
    line = re.sub(r'\s*#.*', '', line)
    return line
