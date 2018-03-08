import logging

from django.conf import settings


def get_logger(name):
    return logging.getLogger('%s.%s' % (settings.LOGGING_PREFIX, name))
