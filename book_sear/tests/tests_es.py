from es.helper import ElasticHelper
from django.test import TestCase
import random
from test_helper import TestHelper


class SearchTestsSuite(TestCase, TestHelper):
    def setUp(self):
        self.es = ElasticHelper()

    def test_search_exiting_word(self):
        """Validate correct message returned by make_search for existing word"""
        word = 'Poirot'
        message = self.es.make_search(word)
        self.assertIn('Text "%s" was found in:' % word, message)

    def test_invalid_search(self):
        """Validate correct message returned by make_search for non existing word"""
        word = 'Poirot%s' % random.randint(2, 20000)
        message = self.es.make_search(word)
        self.assertIn('Text "%s" not found' % word, message)

    def test_logs_creation(self):
        """Validate correct log creation on make_search"""
        word = 'Poirot'
        self.es.make_search(word)
        self.validate_correct_logs_creation(word)
