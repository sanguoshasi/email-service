from __future__ import print_function
import logging
from simple_email import SimpleEmail
from submit import validate_send_request
from result import ErrorResult

logger = logging.getLogger('email_manager')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('error.log')
fh.setLevel(logging.ERROR)
logger.addHandler(fh)


class EmailMgr(object):
    """
    Email Mgr manages all email services. Each email service is a SimpleEmail class.
    """
    email_services = {}

    def __init__(self, email_service_config, debug=False):
        self.service_name = "SimpleEmail"
        if debug:
            self.debug = debug
            logger.setLevel(logging.DEBUG)
        self.__init_mgr(email_service_config, debug)

    def disable_mailgun(self):
        self.email_services['MailGun'].disable_service()

    def disable_sendgrid(self):
        self.email_services['SendGrid'].disable_service()

    def submit_email(self, message_data, attachment_file=None):
        """
        Validate all fields of email.
        If not valid, return error result.
        If valid, try to call MailGun/SendGrid service first in the email_services dict,
        If succeeded calling MailGun/SendGrid service, then return success.
        Otherwise, call the other service and return result
        """
        customized_fields = dict()
        result = validate_send_request(message_data, customized_fields, attachment_file)
        if result is not None:
            return result
        if message_data.get('skip_sendgrid'):
            self.disable_sendgrid()

        service_result = self.try_all_services(customized_fields)
        return service_result or ErrorResult("Sorry! We cannot send email for now. Please try later.")

    def try_all_services(self, message_data):
        for service_name, email_service in self.email_services.iteritems():
            if not email_service.disabled:
                service_result = email_service.send(message_data)
                logger.debug("Returning result from % status: %s, message %s " % (
                    email_service.service_name, service_result.status, service_result.message))
                if service_result.status == "success":
                    return service_result
        return None

    # Create based on class name:
    def __init_mgr(self, email_service_config, debug=False):
        for service_name, email_service in email_service_config.iteritems():
            logger.info("Manager is starting %s service" % service_name)
            self.email_services[service_name] = SimpleEmail.factory(service_name, email_service.get('key'), email_service.get('base_url'), debug)

