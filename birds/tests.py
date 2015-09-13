from django.test import TestCase

import range_grammar
# from birds.data import read_ebird_csv


class TestRangeGrammar(TestCase):

    # Test range_grammar.preprocess
    def test_preprocess_cardinal(self):
        test_string = "S Kenya and e Tanzania"
        result = range_grammar.preprocess(test_string)
        self.assertEquals(result, "southern kenya and eastern tanzania")

    def test_preprocess_ordinal(self):
        test_string = "Desert puna of se Peru, sw Bolivia and nw Argentina"
        result = range_grammar.preprocess(test_string)
        self.assertEquals(result, "desert puna of southeastern peru, southwestern bolivia and northwestern argentina")

    def test_preprocess_multiple_ranges(self):
        test_string = "S Ethiopia to Somalia and adjacent ne Kenya"
        result = range_grammar.preprocess(test_string)
        self.assertEquals(result, "southern ethiopia to somalia and adjacent northeastern kenya")

    def test_preprocess_no_adjectives(self):
        test_string = "Andes of central Peru to Bolivia"
        result = range_grammar.preprocess(test_string)
        self.assertEquals(result, test_string.lower())

    # # Test range_grammar.make_grammar
    # def test_make_grammar_conjunction(self):
    #     test_string = "S Chile, s Argentina and Falkland Islands"
    #     grammar = range_grammar.make_grammar()
    #     test_string = range_grammar.preprocess(test_string)
    #     # import ipdb; ipdb.set_trace()
    #     result = grammar.parseString(test_string)
    #     expected_result = [['southern', 'chile'],
    #                        ['southern', 'argentina'],
    #                        ['falkland islands']]
    #     self.assertEquals(result, expected_result)

    # def test_make_grammar_conjunction_fill(self):
    #     test_string = "Costa Rica to Brazil; Africa, Madagascar and Comoro Islands"
    #     result = range_grammar.make_grammar(test_string)
    #     expected_result = [['Costa Rica', 'to', 'Brazil'], ['Africa'], ['Madagascar', 'Comoro Islands']]
    #     self.assertEquals(result, expected_result)

    # def test_make_grammar_semicolon(self):
    #     test_string = "French Guiana and extreme ne Brazil; e Peru and nw Brazil"
    #     result = range_grammar.make_grammar(test_string)
    #     expected_result = [['French Guiana'], ['extreme', 'northeastern', 'Brazil'], ['eastern Peru', 'northwestern Brazil']]
    #     self.assertEquals(result, expected_result)

    # def test_make_grammar_single_fill(self):
    #     test_string = "E Bolivia to Paraguay, s Brazil and n Argentina"
    #     result = range_grammar.make_grammar(test_string)
    #     expected_result = [['eastern Bolivia', 'to', 'Paraguay'], ['southern Brazil', 'northern Argentina']]
    #     self.assertEquals(result, expected_result)

    # def test_make_grammar_multiple_fill(self):
    #     test_string = "lowlands from northern Mexico south, west of the Andes, to southwestern Ecuador and, east of the Andes, to northeastern Argentina and Brazil"
    #     result = range_grammar.make_grammar(test_string)
    #     expected_result = [['lowlands', 'from', 'northern Mexico'], ['south'], ['west', 'of', 'the', 'Andes', 'to', 'southwestern Ecuador'], ['east', 'of', 'the', 'Andes', 'to', 'northeastern Argentina', ['Brazil']]]
    #     self.assertEquals(result, expected_result)

    # def test_make_grammar_parenthetical_with_fill(self):
    #     test_string = "Coastal se Brazil (Minas Gerais to Rio Grande do Sul)"
    #     result = range_grammar.make_grammar(test_string)
    #     expected_result = []
    #     self.assertEquals(result, expected_result)

    # def test_make_grammar_parenthetical_with_conjunction(self):
    #     test_string = "Andes of nw Argentina (Jujuy and La Rioja)"
    #     result = range_grammar.make_grammar(test_string)
    #     expected_result = []
    #     self.assertEquals(result, expected_result)


class TestReadData(TestCase):

    def test_save_record(self):
        pass

    def test_create_object(self):
        pass
