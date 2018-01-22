import mock
import os
import unittest

from email_service import create_app
from email_service.simple_email import SendGridEmail, MailgunEmail
from email_service.submit import INVALID_SENDER_EMAIL, INVALID_RECIPIENT_EMAIL
from testMessages import *
from utils import assert_success_result, assert_error_result, success_response_side_effect, invalid_to_email_side_effect, invalid_from_email_side_effect


class MailgunAndSendGridTests(unittest.TestCase):
    """Test cases for mailgun and sendgrid."""

    def setUp(self):
        # set config
        self.app = create_app().test_client()
        app_settings = os.getenv(
            'EMAIL_SERVICE_SETTINGS', 'email_service.config.TestingConfig')
        self.app.application.config.from_object(app_settings)

        self.mailgun_api = self.app.application.config.get('EMAIL_SERVICES').get('MailGun').get('key')
        self.mailgun_base_url = self.app.application.config.get('EMAIL_SERVICES').get('MailGun').get('base_url')
        self.sendgrid_api = self.app.application.config.get('EMAIL_SERVICES').get('SendGrid').get('key')

    def test_mailgun_send(self):
        result = MailgunEmail(self.mailgun_api, self.mailgun_base_url).send(valid_message)
        assert_success_result(result)

        result = MailgunEmail(self.mailgun_api, self.mailgun_base_url).send(message_with_empty_subject)
        assert_success_result(result)

    def test_mailgun_send_error(self):
        result = MailgunEmail(self.mailgun_api, self.mailgun_base_url).send(message_with_empty_to_email)
        assert_error_result(result, "'to' parameter is not a valid address. please check documentation")

        result = MailgunEmail(self.mailgun_api, self.mailgun_base_url).send(message_with_invalid_from_email)
        assert_error_result(result, "'from' parameter is not a valid address. please check documentation")

        result = MailgunEmail(self.mailgun_api, self.mailgun_base_url).send(message_with_invalid_to_email)
        assert_error_result(result, "'to' parameter is not a valid address. please check documentation")

        result = MailgunEmail(self.mailgun_api, self.mailgun_base_url).send(message_with_empty_from_email)
        assert_error_result(result, "'from' parameter is not a valid address. please check documentation")

        result = MailgunEmail(self.mailgun_api, self.mailgun_base_url).send(message_with_empty_content)
        assert_error_result(result, "Need at least one of 'text' or 'html' parameters specified")


    @mock.patch("email_service.simple_email.SendGridEmail.send")
    def test_sendgrid_send(self, send):
        send.side_effect = success_response_side_effect()
        result = SendGridEmail(self.sendgrid_api).send(valid_message)
        assert_success_result(result)

    @mock.patch("email_service.simple_email.SendGridEmail.send")
    def test_sendgrid_send_error(self, send):

        send.side_effect = invalid_to_email_side_effect()
        result = SendGridEmail(self.sendgrid_api).send(message_with_empty_to_email)
        assert_error_result(result, INVALID_RECIPIENT_EMAIL)

        send.side_effect = invalid_to_email_side_effect()
        result = SendGridEmail(self.sendgrid_api).send(message_with_invalid_to_email)
        assert_error_result(result, INVALID_RECIPIENT_EMAIL)

        send.side_effect = invalid_from_email_side_effect()
        result = SendGridEmail(self.sendgrid_api).send(message_with_empty_from_email)
        assert_error_result(result, INVALID_SENDER_EMAIL)

        send.side_effect = invalid_from_email_side_effect()
        result = SendGridEmail(self.sendgrid_api).send(message_with_invalid_from_email)
        assert_error_result(result, INVALID_SENDER_EMAIL)

