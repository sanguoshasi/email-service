import mock
import os
import unittest

from email_service.simple_email import MailgunEmail, SendGridEmail
from email_service.result import ErrorResult
from email_service.submit import validate_send_request,\
    INVALID_RECIPIENT_EMAIL, INVALID_SENDER_EMAIL, SUBJECT_CANNOT_BE_EMPTY, CONTENT_CANNOT_BE_EMPTY, SUBJECT_TOO_LONG, CONTENT_TOO_LONG
from email_service.email_manager import EmailMgr
from email_service import create_app
from testMessages import *
from utils import assert_success_result


class RequestTests(unittest.TestCase):
    """Test case for requests."""

    def setUp(self):
        self.app = create_app().test_client()
        app_settings = os.getenv(
            'EMAIL_SERVICE_SETTINGS', 'email_service.config.TestingConfig')
        self.app.application.config.from_object(app_settings)
        self.email_mgr = EmailMgr(self.app.application.config.get('EMAIL_SERVICES'))

    def test_validate_send_request(self):
        assert not validate_send_request(valid_message)
        assert INVALID_RECIPIENT_EMAIL == validate_send_request(message_with_empty_to_email).message
        assert INVALID_RECIPIENT_EMAIL == validate_send_request(message_with_invalid_to_email).message
        assert INVALID_SENDER_EMAIL == validate_send_request(message_with_empty_from_email).message
        assert INVALID_SENDER_EMAIL == validate_send_request(message_with_invalid_from_email).message
        assert SUBJECT_CANNOT_BE_EMPTY == validate_send_request(message_with_empty_subject).message
        assert CONTENT_CANNOT_BE_EMPTY == validate_send_request(message_with_empty_content).message
        assert SUBJECT_TOO_LONG == validate_send_request(message_with_empty_too_long_subject).message
        assert CONTENT_TOO_LONG == validate_send_request(message_with_empty_too_long_content).message

    @mock.patch.object(MailgunEmail, 'send')
    def test_using_mandrill(self, mailgun_send):
        mailgun_send.return_value = ErrorResult("error message")
        result = self.email_mgr.submit_email(valid_message)
        assert_success_result(result)

    @mock.patch.object(SendGridEmail, 'send')
    def test_using_sendgrid(self, sendgrid_send):
        sendgrid_send.return_value = ErrorResult("error message")
        result = self.email_mgr.submit_email(valid_message)
        assert_success_result(result)

    @mock.patch.object(MailgunEmail, 'send')
    @mock.patch.object(SendGridEmail, 'send')
    def test_both_mailgun_mandrill_error(self, sendgrid_send, mailgun_send):
        sendgrid_send.return_value = ErrorResult("sendgrid error message")
        mailgun_send.return_value = ErrorResult("mailgun error message")
        result = self.email_mgr.submit_email(valid_message)
        assert result.status_code == 400
        assert result.status == 'error'
        assert result.message == "Sorry! We cannot send email for now. Please try later."
