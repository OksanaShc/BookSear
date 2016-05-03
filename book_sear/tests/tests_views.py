from book_sear.views import search, search_started, send_email
from test_helper import TestHelper
from django.test import TestCase, RequestFactory, override_settings
import re
import httplib
import random
import email

e_mail = 'test@test.com'


class ViewsTestSuite(TestCase, TestHelper):
    def setUp(self):
        self.factory = RequestFactory()

    def test_search_get(self):
        """Validate correct response on GET request to search view"""
        request = self.factory.get('/')
        response = search(request)

        self.assertEqual(httplib.OK, response.status_code,
                         'Incorrect response status code. Expected: %s. Actual: %s' %
                         (httplib.OK, response.status_code))

        title_reg = re.compile("<title>(.+?)</title>")
        title = title_reg.search(response.content).group(1)
        self.assertEqual(title, 'Search',
                         'Incorrect page title. Expected: "Search". Actual: "%s"' % title)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend',
                       EMAIL_FILE_PATH='tmp/email-messages/')
    def test_search_post_min_len(self):
        """Validate correct response and e_mail creation on POST request """\
        """with min len (1) of search text to search view"""

        target_text = 'I'
        request = self.factory.post('/', {'e_mail': e_mail, 'target_text': target_text})
        response = search(request)

        self.assertEqual(httplib.OK, response.status_code,
                         'Incorrect response status code. Expected: %s. Actual: %s' %
                         (httplib.OK, response.status_code))

        self.assertIn("Search started. Results will be sent to '%s'" % e_mail, response.content)

        self.validate_correct_email_creation(e_mail, target_text)

    def test_search_post_logs_creation(self):
        """Validate correct log creation on POST request """
        target_text = 'test %s' % random.randint(1, 90000)
        request = self.factory.post('/', {'e_mail': e_mail, 'target_text': target_text})
        response = search(request)

        self.validate_correct_logs_creation(target_text)

    def test_search_post_without_text_for_search(self):
        """Validate correct response on POST request without search text to search view"""

        request = self.factory.post('/', {'e_mail': e_mail, 'target_text': ''})
        response = search(request)

        self.assertEqual(httplib.BAD_REQUEST, response.status_code,
                         'Incorrect response status code. Expected: %s. Actual: %s' %
                         (httplib.BAD_REQUEST, response.status_code))
        self.assertRegexpMatches(response.content, "Such fields contain errors:.*target_text.*This field is required")

    def test_search_post_without_e_mail(self):
        """Validate correct response on POST request without e_mail to search view"""

        request = self.factory.post('/', {'e_mail': '', 'target_text': 'text'})
        response = search(request)

        self.assertEqual(httplib.BAD_REQUEST, response.status_code,
                         'Incorrect response status code. Expected: %s. Actual: %s' %
                         (httplib.BAD_REQUEST, response.status_code))
        self.assertRegexpMatches(response.content, "Such fields contain errors:.*e_mail.*This field is required")

    def test_search_post_without_e_mail_and_text_for_search(self):
        """Validate correct response on POST request without e_mail and text to search view"""

        request = self.factory.post('/', {'e_mail': '', 'target_text': ''})
        response = search(request)

        self.assertEqual(httplib.BAD_REQUEST, response.status_code,
                         'Incorrect response status code. Expected: %s. Actual: %s' %
                         (httplib.BAD_REQUEST, response.status_code))
        self.assertRegexpMatches(response.content,
                                 """Such fields contain errors:.*target_text.*"""
                                 """This field is required.*e_mail.*This field is required""")

    def test_search_started(self):
        """Validate correct response on request to search_started view"""

        request = self.factory.get('')
        response = search_started(request)
        self.assertEqual(httplib.OK, response.status_code,
                         'Incorrect response status code. Expected: %s. Actual: %s' %
                         (httplib.OK, response.status_code))

        title_reg = re.compile("<title>(.+?)</title>")
        title = title_reg.search(response.content).group(1)
        self.assertEqual(title, 'Search started',
                         'Incorrect page title. Expected: "Search started". Actual: "%s"' % title)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend',
                       EMAIL_FILE_PATH='tmp/email-messages/')
    def test_send_email_with_empty_e_mail_field(self):
        """Validate correct response send_email if to_emai field is empty"""
        response = send_email('', 'test message')
        self.assertEqual(httplib.BAD_REQUEST, response.status_code,
                         'Incorrect response status code. Expected: %s. Actual: %s' %
                         (httplib.BAD_REQUEST, response.status_code))

        self.assertIn('Make sure all fields are entered and valid', response.content)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend',
                       EMAIL_FILE_PATH='tmp/email-messages/')
    def test_send_email_with_empty_text_field(self):
        """Validate correct response send_email if text field is empty"""
        response = send_email(e_mail, '')
        self.assertEqual(httplib.BAD_REQUEST, response.status_code,
                         'Incorrect response status code. Expected: %s. Actual: %s' %
                         (httplib.BAD_REQUEST, response.status_code))

        self.assertIn('Make sure all fields are entered and valid', response.content)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend',
                       EMAIL_FILE_PATH='tmp/email-messages/')
    def test_send_email_with_empty_text_and_e_mail_fields(self):
        """Validate correct response send_email if text and e_mail fields are empty"""
        response = send_email(e_mail, '')
        self.assertEqual(httplib.BAD_REQUEST, response.status_code,
                         'Incorrect response status code. Expected: %s. Actual: %s' %
                         (httplib.BAD_REQUEST, response.status_code))

        self.assertIn('Make sure all fields are entered and valid', response.content)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend',
                       EMAIL_FILE_PATH='tmp/email-messages/')
    def test_send_email_with_valid_text_and_e_mail_fields(self):
        """Validate correct response send_email with valid text and e_mail fields"""

        target_text = 'test_text'
        send_email(e_mail, target_text)

        e_mail_file_path = self.get_latest_e_mail_file()

        with open(e_mail_file_path) as e_mail_text:
            e_mail_send = email.message_from_file(e_mail_text)
        self.assertEqual(e_mail_send.get('To'), e_mail)
        self.assertEqual(e_mail_send.get('Subject'), 'search results')
        self.assertIn(target_text, e_mail_send.get_payload())
