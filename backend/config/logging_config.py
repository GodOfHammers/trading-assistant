# backend/config/logging_config.py

import logging.config
import os

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/stock_trading.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': True
        },
        'trading_engine': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': False
        },
        'news_analyzer': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

def setup_logging():
    """Set up logging configuration"""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Apply configuration
    logging.config.dictConfig(LOGGING_CONFIG)