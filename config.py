"""
Config for SendGrid and MailGun email services
"""


class BaseConfig(object):
    """Base configuration."""
    DEBUG = False
    SENDGRID_API_KEY = # Put your SnedGrid API key here
    MAILGUN_MESSAGE_BASE_URL = #Put your MailGun base URL here
    MAILGUN_API_KEY = # Put your MailGun API key here

    # Email Service names
    EMAIL_SERVICES = {
        'MailGun': {
            'key': MAILGUN_API_KEY,
            'base_url': MAILGUN_MESSAGE_BASE_URL
        },
        'SendGrid': {
            'key': SENDGRID_API_KEY
        }
    }


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
