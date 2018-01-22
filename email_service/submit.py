from __future__ import print_function
from validate_email import validate_email
from result import ErrorResult
import logging, os

logger = logging.getLogger('simple_email')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('error.log')
fh.setLevel(logging.ERROR)
logger.addHandler(fh)

MAX_SUBJECT_LENGTH = 1000
MAX_CONTENT_LENGTH = 10000
MAX_CC_EMAIL_LENGTH = 100
MAX_ATTACHMENT_CONTENT_LENGTH = 25 * 1024 * 1024

TO_EMAIL = 'to_email'
FROM_EMAIL = 'from_email'
SUBJECT = 'subject'
CONTENT = 'content'
CC_EMAILS = 'cc_emails'
CC_EMAIL_LIST = 'cc_email_list'
ATTACHMENT_FILE = 'attachment_file'

INVALID_RECIPIENT_EMAIL = 'invalid recipient email'
INVALID_SENDER_EMAIL = 'invalid sender email'
INVALID_CC_EMAIL = 'invalid cc email'
SUBJECT_CANNOT_BE_EMPTY = 'subject cannot be empty'
SUBJECT_TOO_LONG = 'subject cannot be more than %s characters' % MAX_SUBJECT_LENGTH
CONTENT_CANNOT_BE_EMPTY = 'content cannot be empty'
CONTENT_TOO_LONG = 'content cannot be more than %s characters' % MAX_CONTENT_LENGTH
CC_EMAILS_TOO_LONG = 'cc emails could not be more than %s recipients' % MAX_CC_EMAIL_LENGTH
ATTACHMENT_TOO_LARGE = 'attachment is too large'


def validate_send_request(message_data, customized_dict={}, attachment_file=None):
    if not validate_email(message_data[TO_EMAIL]):
        return ErrorResult(INVALID_RECIPIENT_EMAIL)
    customized_dict[TO_EMAIL] = message_data[TO_EMAIL]

    if not validate_email(message_data[FROM_EMAIL]):
        return ErrorResult(INVALID_SENDER_EMAIL)
    customized_dict[FROM_EMAIL] = message_data[FROM_EMAIL]

    if message_data[SUBJECT] == "":
        return ErrorResult(SUBJECT_CANNOT_BE_EMPTY)
    elif len(message_data[SUBJECT]) > MAX_SUBJECT_LENGTH:
        return ErrorResult(SUBJECT_TOO_LONG)
    customized_dict[SUBJECT] = message_data[SUBJECT]

    if message_data[CONTENT] == "":
        return ErrorResult(CONTENT_CANNOT_BE_EMPTY)
    elif len(message_data[CONTENT]) > MAX_CONTENT_LENGTH:
        return ErrorResult(CONTENT_TOO_LONG)
    customized_dict[CONTENT] = message_data[CONTENT]

    if message_data.get(CC_EMAILS):
        cc_email_list = [x.strip() for x in message_data[CC_EMAILS].split(',')]
        if len(cc_email_list) > MAX_CC_EMAIL_LENGTH:
            return ErrorResult(CC_EMAILS_TOO_LONG)
        for email in cc_email_list:
            if not validate_email(email):
                return ErrorResult(INVALID_CC_EMAIL)
        customized_dict[CC_EMAIL_LIST] = cc_email_list

    if attachment_file:
        if not validate_attachment(attachment_file):
            return ErrorResult(ATTACHMENT_TOO_LARGE)
        customized_dict[ATTACHMENT_FILE] = attachment_file


def validate_attachment(attachment_file):
    attachment_file.seek(0, os.SEEK_END)
    file_length = attachment_file.tell()
    if file_length > MAX_ATTACHMENT_CONTENT_LENGTH:
        return False
    return True

