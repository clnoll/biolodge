import os
import re
from itertools import ifilter
from itertools import imap

from pyparsing import Keyword
from pyparsing import And
from pyparsing import Or


def Phrase(string):
    return And(map(Keyword, string.split()))


def one_of_keywords(strings):
    return _one_of_strings(strings, Keyword)


def one_of_keywords_in_file(path):
    return _one_of_strings_in_file(path, Keyword)


def one_of_phrases(strings):
    return _one_of_strings(strings, Phrase)


def one_of_phrases_in_file(path):
    return _one_of_strings_in_file(path, Phrase)


def _one_of_strings_in_file(path, cls):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        path)
    with open(path) as fp:
        return _one_of_strings(read_lines(fp), cls)


def _one_of_strings(strings, cls):
    return Or(imap(cls, strings))


def read_lines(fp):
    return ifilter(None, imap(_process_line, fp))


def _process_line(line):
    line = line.strip()
    line = line.decode('utf8')
    # Strip inline comments
    line = re.sub(r'\s*#.*', '', line)
    return line
