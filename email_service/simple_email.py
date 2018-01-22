import logging, requests
import sendgrid
from sendgrid.helpers.mail import Email, Attachment, Content, Mail, Personalization
from python_http_client import exceptions
import urllib2
from abc import ABCMeta, abstractmethod
from result import ErrorResult, Result, SuccessResult
import base64

#set up log
logger = logging.getLogger('simple_email')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('error.log')
fh.setLevel(logging.ERROR)
logger.addHandler(fh)

success_result_obj = SuccessResult("Email sent successfully!")


class SimpleEmail(object):
    __metaclass__ = ABCMeta

    def __init__(self, api_key, debug=False):
        self.service_name = "SimpleEmail"
        self.disabled = False
        self.api_key = api_key
        if debug:
            logger.handlers = []
            logger.addHandler(logging.StreamHandler())
            logger.setLevel(logging.DEBUG)

    # Create based on class name:
    @staticmethod
    def factory(service_name, api_key, base_url=None, debug=False):
        if service_name == "MailGun":
            logger.info("Starting MailGun Email service with base_url: %s" % base_url)
            return MailgunEmail(api_key, base_url, debug=debug)
        if service_name == "SendGrid":
            logger.info("Starting SendGrid Email service with base_url: %s" % base_url)
            return SendGridEmail(api_key, debug=debug)
        assert 0, "Bad service creation: " + service_name

    @abstractmethod
    def send(self, message):
        pass

    def disable_service(self):
        self.disabled = True


class MailgunEmail(SimpleEmail):

    def __init__(self, api_key, base_url, debug=False):
        super(MailgunEmail, self).__init__(api_key, debug)
        self.service_name = 'MailGun'
        self.base_url = base_url

    def send(self, message_data):
        """
        Send email using Mailgun

        Args:
           message_data : contains the information about the email will be sent::
                from_email (string): the sender email address.
                to_email (string): the email address of the recipient (only have one recipient for now)
                content (string): full text content to be sent
                subject (string): the message subject (optional)

        Returns:
            a SuccessResult object for success and a ErrorResult object for failure

        Note: With the current setup, responses with 400 error code will not be returned since Mailgun returns 400 error only when there's a
              invalid email or empty content but we already done validation before calling this method.

              Changing this function e.g. adding new email parameters may cause 400 error, so make sure to check the official documentation of
              Mailgun to see if it will return 400 error and handle them correctly.

              All errors are caught and the responses are logged
        """

        logger.debug("Starting to call Mailgun to send the email")
        to_email_list = [message_data['to_email'], message_data.get('cc_email_list')]

        files = []
        if 'attachment_file' in message_data:
            attachment_file = message_data['attachment_file']
            files = [("attachment", (attachment_file.filename, attachment_file.read()))]

        r = requests.post(
            self.base_url,
            auth=("api", self.api_key),
            files=files,
            data={"from": message_data['from_email'],
                  "to": to_email_list,
                  "subject": message_data['subject'],
                  "text": message_data['content']})
        status_code = r.status_code
        json_response = r.json()
        response_message = json_response['message']
        logger.debug("Getting result from calling Mailgun: response code: %s, message: %s " % (status_code,response_message))
        self.track(message_data, {'status_code': status_code, 'message': response_message})
        if status_code == 200:
            return success_result_obj
        else:
            return ErrorResult(response_message, status_code)

    @staticmethod
    def track(message_data, response):
        if response['status_code'] == 200:
            logger.info('Sender %s sent out email successfully to %s by MailGun service.' % (
                message_data.get('from_email'), message_data.get('to_email')))
        else:
            logger.error(
                "Get an unexpected status: %s when calling MailGun Email to send the email with message %s!" % (
                    response.get('status_code'), response.get('message')))


class SendGridEmail(SimpleEmail):

    def __init__(self, api_key, debug=False):
        super(SendGridEmail, self).__init__(api_key, debug)
        self.sg_client = sendgrid.SendGridAPIClient(apikey=api_key)
        self.service_name = 'SendGrid'

    def send(self, message_data):
        """Send email by SendGrid client

        Args:
            message_data : contains the information about the email will be sent::
                from_email (string): the sender email address.
                to_email (string): the email address of the recipient (only have one recipient for now)
                content (string): full text content to be sent
                subject (string): the message subject
                attachment: attachment object from email
                personalization: contains cc, bcc

        Returns:
            a SuccessResult object for success and a ErrorResult object for failure
            For the failure case, result is generated based on HTTP status code
        """

        from_email = Email(message_data['from_email'])
        to_email = Email(message_data['to_email'])
        subject = message_data['subject']
        content = Content("text/plain", message_data['content'])
        mail = Mail(from_email, subject, to_email, content)
        if 'attachment_file' in message_data:
            attachment = self.build_attachment(file=message_data['attachment_file'])
            mail.add_attachment(attachment)
        if 'cc_email_list' in message_data:
            personalization = self.get_personalization_dict(message_data['cc_email_list'])
            mail.add_personalization(self.build_personalization(personalization))

        try:
            logger.debug("Starting to call SendGridEmail to send the email")
            response = self.sg_client.client.mail.send.post(request_body=mail.get())
            logger.debug("Get result back from SendGridEmail: %s " % response)
        except urllib2.HTTPError as e:
            logger.exception("Get an exception when calling SendGridEmail to send the email!")
            return ErrorResult(e.message)
        except exceptions.BadRequestsError as e:
            logger.exception("Get an exception when calling SendGridEmail to send the email!")
            return ErrorResult(e.message)
        self.track(message_data, response)
        if response.status_code == 202:
            return success_result_obj
        else:
            return Result(response.status_code, "Get an unexpected status from SendGridEmail!")

    @staticmethod
    def build_personalization(pers):
        """Build personalization instance from a dict"""
        personalization = Personalization()
        if 'to_list' in pers:
            for to_addr in pers['to_list']:
                personalization.add_to(to_addr)
        if 'cc_list' in pers:
            for cc_addr in pers['cc_list']:
                personalization.add_to(cc_addr)
        if 'bcc_list' in pers:
            for bcc_addr in pers['bcc_list']:
                personalization.add_bc(bcc_addr)

        if 'headers' in pers:
            for header in pers['headers']:
                personalization.add_header(header)

        if 'substitutions' in pers:
            for substitution in pers['substitutions']:
                personalization.add_substitution(substitution)

        if 'custom_args' in pers:
            for arg in pers['custom_args']:
                personalization.add_custom_arg(arg)

        if 'subject' in pers:
            personalization.subject = pers['subject']

        if 'send_at' in pers:
            personalization.send_at = pers['send_at']
        return personalization

    @staticmethod
    def get_personalization_dict(cc_emails):
        """Get a dict of personalization."""
        pers = dict()
        pers['cc_list'] = [Email(x) for x in cc_emails]
        return pers

    @staticmethod
    def build_attachment(attachment_file):
        """Build attachment """
        attachment = Attachment()
        attachment.content = base64.b64encode(attachment_file.read())
        attachment.type = attachment_file.content_type
        attachment.filename = attachment_file.filename
        return attachment

    @staticmethod
    def track(message_data, response):
        if response.status_code == 202:
            logger.info('Sender %s sent out email successfully to %s by SendGrid service!' % (
                message_data.get('from_email'), message_data.get('to_email')))
        else:
            logger.error(
                "Get an unexpected status: %s when calling SendGridEmail to send the email!" % response['status_code'])
