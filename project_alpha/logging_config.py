import logging
import logging.config
import os

def setup_logging(default_level=logging.INFO):
    """
    Setup logging configuration
    """
    log_folder = "logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'json': {
                'format': '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(name)s", "message": "%(message)s"}'
            }
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(log_folder, 'app.log'),
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'formatter': 'json'
            }
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console', 'file'],
                'level': default_level,
                'propagate': True
            },
            'scapy.runtime': {  # Suppress Scapy IPv6 warnings
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False
            }
        }
    }

    logging.config.dictConfig(logging_config)
    logging.info("Logging configured successfully")
