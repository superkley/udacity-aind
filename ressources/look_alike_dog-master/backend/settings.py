"""Application configuration."""
import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('LOOK_ALIKE_DOG_SECRET', 'OKWD@!-CHANGE-ME-IN-YOUR-CODE')
    APP_DIR = os.path.abspath(os.path.dirname(__file__)) # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir)) # Project root directory


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
