import os
import socket

from dotenv import load_dotenv, find_dotenv

dotenv_file = find_dotenv()
if dotenv_file:
    load_dotenv(dotenv_file)

APP_NAME = 'videalize'
ENV = os.environ.get('VIDEALIZE_ENV', 'dev')
HOSTNAME = socket.gethostname()

REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/3')
REDIS_PROCESS_VIDEO_QUEUE = os.environ.get('REDIS_QUEUE', 'process_video')
REDIS_TEMP_VIDEO_QUEUE = os.environ.get('REDIS_TEMP_QUEUE', 'processing_{0}'.format(HOSTNAME))

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

MAX_RETRIES = 3
