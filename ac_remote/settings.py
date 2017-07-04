import os

SUBSCRIBE_KEY = os.environ.get('SUBSCRIBE_KEY')
PUBLISH_KEY = os.environ.get('PUBLISH_KEY')

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
LOG_FILE = os.environ.get('LOG_FILE', '')
