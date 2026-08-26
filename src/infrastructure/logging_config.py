import logging.config
import sys


def setup_logging(log_level: str = 'INFO'):
    """
    Centralized logger configuration for Dev and Prod.

    :param log_level: The loglevel to show.
    :type log_level: str
    """

    log_format = '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'

    log_formatters = {
        'default': {
            'format': log_format,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    }

    log_handlers = {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'default',
            'level': log_level,
        },
    }

    loggers = {
        'uvicorn': {
            'handlers': ['console'],
            'level': log_level,
            'propagate': False,
        },
        'uvicorn.access': {
            'handlers': ['console'],
            'level': log_level,
            'propagate': False,
        },
        'fastapi': {
            'handlers': ['console'],
            'level': log_level,
            'propagate': False,
        },
    }

    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': log_formatters,
        'handlers': log_handlers,
        'root': {
            'handlers': ['console'],
            'level': log_level,
        },
        'loggers': loggers,
    }

    logging.config.dictConfig(config)
