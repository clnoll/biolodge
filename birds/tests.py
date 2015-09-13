from django.test import TestCase

import parse_range
from birds.data import read_ebird_csv


class TestRangeGrammar(TestCase):

    # Test parse_range.preprocess
    def test_preprocess_cardinal(self):
        test_string = "S Kenya and e Tanzania"
        result = parse_range.preprocess(test_string)
        self.assertEquals(result, "southern Kenya and eastern Tanzania")

    def test_preprocess_ordinal(self):
        test_string = "Desert puna of se Peru, sw Bolivia and nw Argentina"
        result = parse_range.preprocess(test_string)
        self.assertEquals(result, "Desert puna of southeastern Peru, southwestern Bolivia and northwestern Argentina")

    def test_preprocess_multiple_ranges(self):
        test_string = "S Ethiopia to Somalia and adjacent ne Kenya"
        result = parse_range.preprocess(test_string)
        self.assertEquals(result, "southern Ethiopia to Somolia and adjacent northeastern Kenya")

    def test_preprocess_no_adjectives(self):
        test_string = "Andes of central Peru to Bolivia"
        result = parse_range.preprocess(test_string)
        self.assertEquals(result, test_string)

    # Test parse_range.make_grammar
    def test_make_grammar_single_range(self):
        test_string = ""
        result = parse_range.make_grammar(test_string)
        self.assertEquals(result, "")

    def test_make_grammar_multiple ranges(self):
        test_string = ""
        result = parse_range.make_grammar(test_string)
        self.assertEquals(result, "")

    def test_make_grammar_single_fill(self):
        test_string = ""
        result = parse_range.make_grammar(test_string)
        self.assertEquals(result, "")

    def test_make_grammar_multiple_fill(self):
        test_string = ""
        result = parse_range.make_grammar(test_string)
        self.assertEquals(result, "")

    def test_make_grammar_parenthetical(self):
        test_string = ""
        result = parse_range.make_grammar(test_string)
        self.assertEquals(result, "")


class TestReadData(TestCase):

    def test_save_record(self):
        pass

    def test_create_object(self):
        pass
