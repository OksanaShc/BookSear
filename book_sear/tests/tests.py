from django.test import TestCase, Client, override_settings
import re
import httplib
import random
import os
import email
from test_helper import TestHelper

e_mail = 'test@test.com'
existing_text = 'Madame changed her room almost immediately after the crime'
log_file_name = 'search_result.log'


class IntegrationTestingSuite(TestCase, TestHelper):

    def setUp(self):
        self.c = Client()

    def test_starting_page(self):
        """Validate correct status code and title of starting page"""

        response = self.c.get('/')
        self.assertEqual(httplib.OK, response.status_code,
                         'Incorrect response status code. Expected: %s. Actual: %s' %
                         (httplib.OK, response.status_code))

        title_reg = re.compile("<title>(.+?)</title>")
        title = title_reg.search(response.content).group(1)
        self.assertEqual(title, 'Search', 'Incorrect page title. Expected: "Search". Actual: "%s"' % title)

    def test_valid_search_request_response(self):
        """"Validate correct status code and page text for valid search request"""

        response = self.c.post('/', {'e_mail': e_mail, 'target_text': existing_text})
        self.assertEqual(httplib.OK, response.status_code,
                         'Incorrect response status code. Expected: %s. Actual: %s' %
                         (httplib.OK, response.status_code))
        self.assertIn("Search started. Results will be sent to '%s'" % e_mail, response.content)

    def test_search_logs_creation_non_existing_text(self):
        """Validate correct logs creation for not existing text search"""

        target_text = 'my text %s' % random.randint(1, 10000)
        response = self.c.post('/', {'e_mail': e_mail, 'target_text': target_text})

        self.assertEqual(httplib.OK, response.status_code,
                         'Incorrect response status code. Expected: %s. Actual: %s' %
                         (httplib.OK, response.status_code))

        self.validate_correct_logs_creation(target_text)

    def test_search_logs_creation_existing_text(self):
        """Validate correct logs creation for existing text search"""

        response = self.c.post('/', {'e_mail': e_mail, 'target_text': existing_text})

        self.assertEqual(httplib.OK, response.status_code,
                         'Incorrect response status code. Expected: %s. Actual: %s' %
                         (httplib.OK, response.status_code))

        self.validate_correct_logs_creation(existing_text)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend',
                       EMAIL_FILE_PATH='tmp/email-messages/')
    def test_e_mail_creation_for_non_exiting_text(self):
        """Validate correct e_mail creation for not existing text search"""

        target_text = 'my text %s' % random.randint(1, 10000)
        response = self.c.post('/', {'e_mail': e_mail, 'target_text': target_text})

        self.assertEqual(httplib.OK, response.status_code,
                         'Incorrect response status code. Expected: %s. Actual: %s' %
                         (httplib.OK, response.status_code))
        expected_text = 'Text "%s" not found' % target_text
        self.validate_correct_email_creation(e_mail, expected_text)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend',
                       EMAIL_FILE_PATH='tmp/email-messages/')
    def test_e_mail_creation_for_exiting_text(self):
        """Validate correct e_mail creation for existing text search"""

        response = self.c.post('/', {'e_mail': e_mail, 'target_text': existing_text})

        self.assertEqual(httplib.OK, response.status_code,
                         'Incorrect response status code. Expected: %s. Actual: %s' %
                         (httplib.OK, response.status_code))
        expected_text = """Text "%s" was found in: """ \
                        """book murder_on_the_links_by_agatha_christie chapter 28 page 65""" % \
                        existing_text
        self.validate_correct_email_creation(e_mail, expected_text)
