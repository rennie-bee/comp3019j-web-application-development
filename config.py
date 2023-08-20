import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


# The programme writing of config.py studies the instruction in Book
# "FLASK Web Development: Developing Web Applications with Python, Second Edition"

# This class is created to prepare configs
class Config:
    # Email Server configurations are imported from environment variables below.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'difficult to guess string'
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = '13051702828@163.com'
    MAIL_PASSWORD = 'FSDNVOITMJNBLVXM'
    FLASKY_MAIL_SUBJECT_PREFIX = '[CUISINE MONSTER]'
    FLASKY_MAIL_SENDER = '13051702828@163.com'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Another custom made configuration, here is empty
    @staticmethod
    def init_app(app):
        pass


# Development Database URL is configured here.
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    # WTF_CSRF_ENABLED = False
    # Handle with browser not updating automatically
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=2)


# Testing Database URL is configured here.
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite://'


# Production Database URL is configured here.
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


# config dictionary registered different environments(use development as default)
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
