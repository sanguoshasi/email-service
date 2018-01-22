from email_service.submit import TO_EMAIL, FROM_EMAIL, SUBJECT, CONTENT
valid_message = {
    TO_EMAIL: 'lidayun0701@gmail.com',
    FROM_EMAIL: 'uber@gmail.com',
    SUBJECT: SUBJECT,
    CONTENT: 'content to send '
    }

message_with_empty_to_email = {
    TO_EMAIL: '',
    FROM_EMAIL: 'valid@gmail.com',
    SUBJECT: 'email subject ',
    CONTENT: CONTENT
    }

message_with_invalid_to_email = {
    TO_EMAIL: 'invalid_email',
    FROM_EMAIL: 'valid@gmail.com',
    SUBJECT: 'email subject ',
    CONTENT: CONTENT
    }

message_with_empty_from_email = {
    TO_EMAIL: 'lidayun0701@gmail.com',
    FROM_EMAIL: '',
    SUBJECT: 'email subject ',
    CONTENT: CONTENT
    }

message_with_invalid_from_email = {
    TO_EMAIL: 'lidayun0701@gmail.comm',
    FROM_EMAIL: 'invalid_from_email',
    SUBJECT: 'email subject ',
    CONTENT: CONTENT
    }

message_with_empty_content = {
    TO_EMAIL: 'lidayun0701@gmail.com',
    FROM_EMAIL: 'valid@gmail.com',
    SUBJECT: 'email subject',
    CONTENT : ''
    }

message_with_empty_too_long_content = {
    TO_EMAIL: 'lidayun0701@gmail.com',
    FROM_EMAIL: 'valid@gmail.com',
    SUBJECT: SUBJECT,
    CONTENT: 10001 * '.'
    }

message_with_empty_subject = {
    TO_EMAIL: 'lidayun0701@gmail.com',
    FROM_EMAIL: 'valid@gmail.com',
    SUBJECT: '',
    CONTENT: 'content with no subject to send '
    }

message_with_empty_too_long_subject = {
    TO_EMAIL: 'lidayun0701@gmail.com',
    FROM_EMAIL: 'valid@gmail.com',
    SUBJECT: 1001 * '.',
    CONTENT: 'content to send '
    }