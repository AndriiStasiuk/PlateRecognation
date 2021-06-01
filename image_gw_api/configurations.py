"""The app module, containing the app factory function."""

import logging

from image_gw_api.constants import SERVICE_NAME


class Config:
    """Constants for configuration."""

    SERVICE_NAME = SERVICE_NAME
    DEBUG = False
    LOG_LEVEL = logging.DEBUG


class DevConfig(Config):
    """Development configuration."""

    DEBUG = True
