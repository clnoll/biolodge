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
    def test_make_grammar_conjunction(self):
        test_string = ""
        result = parse_range.make_grammar(test_string)
        self.assertEquals(result, "")

    def test_make_grammar_conjunction_fill(self):
        test_string = "Costa Rica to Brazil; Africa, Madagascar and Comoro Islands"
        result = parse_range.make_grammar(test_string)
        self.assertEquals(result, "")

    def test_make_grammar_conjunction_semicolon(self):
        test_string = "French Guiana and extreme ne Brazil; e Peru and nw Brazil"
        result = parse_range.make_grammar(test_string)
        self.assertEquals(result, "")

    def test_make_grammar_single_fill(self):
        test_string = "E Bolivia to Paraguay, s Brazil and n Argentina"
        result = parse_range.make_grammar(test_string)
        self.assertEquals(result, "")

    def test_make_grammar_multiple_fill(self):
        test_string = "lowlands from northern Mexico south, west of the Andes, to southwestern Ecuador and, east of the Andes, to northeastern Argentina and Brazil"
        result = parse_range.make_grammar(test_string)
        self.assertEquals(result, "")

    def test_make_grammar_parenthetical_with_fill(self):
        test_string = "Coastal se Brazil (Minas Gerais to Rio Grande do Sul)"
        result = parse_range.make_grammar(test_string)
        self.assertEquals(result, "")

    def test_make_grammar_parenthetical_with_conjunction(self):
        test_string = "Andes of nw Argentina (Jujuy and La Rioja)"
        result = parse_range.make_grammar(test_string)
        self.assertEquals(result, "")

# skip if "extinct" in raw_location
# if "of" in description, take the word 1 before
# todo:  flags for "breeds" and "winters"

class TestReadData(TestCase):

    def test_save_record(self):
        pass

    def test_create_object(self):
        pass
