import os
import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # JSON formatter for structured logging
    class CustomJsonFormatter(jsonlogger.JsonFormatter):
        def add_fields(self, log_record, record, message_dict):
            super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
            log_record['logger'] = record.name
            log_record['level'] = record.levelname
            log_record['timestamp'] = self.formatTime(record)

    # File handler for JSON logs
    json_handler = RotatingFileHandler(
        'logs/app.json',
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    json_handler.setFormatter(CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s'))
    
    # Console handler for development
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))

    logger.addHandler(json_handler)
    logger.addHandler(console_handler)

    return logger

# Create loggers for different components
app_logger = setup_logger('app')
scraper_logger = setup_logger('scraper')
data_processor_logger = setup_logger('data_processor')

# Example usage:
# app_logger.info('Application started')
# scraper_logger.error('Failed to scrape URL', extra={'url': 'http://example.com'})
# data_processor_logger.warning('Data validation warning', extra={'record_id': 123})