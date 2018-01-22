"""
Config for SendGrid and MailGun email services
"""


class BaseConfig(object):
    """Base configuration."""
    DEBUG = False
    SENDGRID_API_KEY = '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'
    MAILGUN_MESSAGE_BASE_URL = 'https://api.mailgun.net/v3/sannianerban.name/messages'
    MAILGUN_API_KEY = 'key-edec8464563796ba6741c2dc53ea3144'

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
    DOMAIN_SERVICE = 'email.buyongqucai.com'
