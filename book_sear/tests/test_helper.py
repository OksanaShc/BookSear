import os
import time
import email
log_file_name = 'search_result.log'

# Should be used with test class inherited from TestCase

class TestHelper(object):
    @staticmethod
    def get_latest_e_mail_file():
        time.sleep(1) # tests execution is more than log files creation
        logdir = 'tmp/email-messages/'
        logfiles = sorted([f for f in os.listdir(logdir)])
        e_mail_file = logfiles[-1]
        e_mail_file_path = logdir + e_mail_file
        return e_mail_file_path

    def validate_correct_logs_creation(self, searching_text):
        self.assertTrue(os.path.isfile(log_file_name), 'Log file %s was not exists' % log_file_name)
        with open(log_file_name) as log_file:
            logs = log_file.read()
        expected_log = "Search text: '%s'.Search took: \d+ ms" % searching_text
        self.assertRegexpMatches(logs, expected_log, 'Log "%s" not found in %s' % (expected_log, log_file_name))

    def validate_correct_email_creation(self, e_mail_to, expected_text):

        for i in xrange(3):
            try:
                e_mail_file_path = self.get_latest_e_mail_file()

                with open(e_mail_file_path) as e_mail_text:
                    e_mail_send = email.message_from_file(e_mail_text)
                self.assertEqual(e_mail_send.get('To'), e_mail_to)
                self.assertEqual(e_mail_send.get('Subject'), 'search results')

                self.assertIn(expected_text, e_mail_send.get_payload().replace('\n', ' '))
                break
            except Exception, e:
                if i == 2:
                    raise

