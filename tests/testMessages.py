valid_message = {
    'to_email': 'lidayun0701@gmail.com',
    'from_email': 'uber@gmail.com',
    'subject': 'subject',
    'content': 'content to send '
    }

message_with_empty_to_email = {
    'to_email': '',
    'from_email': 'valid@gmail.com',
    'subject': 'email subject ',
    'content': 'content'
    }

message_with_invalid_to_email = {
    'to_email': 'invalid_email',
    'from_email': 'valid@gmail.com',
    'subject': 'email subject ',
    'content': 'content'
    }

message_with_empty_from_email = {
    'to_email': 'lidayun0701@gmail.com',
    'from_email': '',
    'subject': 'email subject ',
    'content': 'content'
    }

message_with_invalid_from_email = {
    'to_email': 'lidayun0701@gmail.comm',
    'from_email': 'invalid_from_email',
    'subject': 'email subject ',
    'content': 'content'
    }

message_with_empty_content = {
    'to_email': 'lidayun0701@gmail.com',
    'from_email': 'valid@gmail.com',
    'subject': 'email subject',
    'content' : ''
    }

message_with_empty_too_long_content = {
    'to_email': 'lidayun0701@gmail.com',
    'from_email': 'valid@gmail.com',
    'subject': 'subject',
    'content': 10001 * '.'
    }

message_with_empty_subject = {
    'to_email': 'lidayun0701@gmail.com',
    'from_email': 'valid@gmail.com',
    'subject': '',
    'content': 'content with no subject to send '
    }

message_with_empty_too_long_subject = {
    'to_email': 'lidayun0701@gmail.com',
    'from_email': 'valid@gmail.com',
    'subject': 1001 * '.',
    'content': 'content to send '
    }