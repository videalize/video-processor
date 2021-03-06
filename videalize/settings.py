import os
from os import path
import socket

from dotenv import load_dotenv, find_dotenv

PROJECT_ROOT = os.environ.get('PROJECT_ROOT', os.getcwd())

ENV = os.environ.get('VIDEALIZE_ENV', 'dev')

if ENV == 'dev':
    dotenv_file = find_dotenv()
    if dotenv_file:
        load_dotenv(dotenv_file)

APP_NAME = 'videalize'
HOSTNAME = socket.gethostname()

REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/3')
REDIS_PROCESS_VIDEO_QUEUE = os.environ.get('REDIS_QUEUE', 'process_video')
REDIS_TEMP_VIDEO_QUEUE = os.environ.get('REDIS_TEMP_QUEUE', 'processing_{0}'.format(HOSTNAME))

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

IBM_USERNAME = os.environ.get('IBM_USERNAME')
IBM_PASSWORD = os.environ.get('IBM_PASSWORD')

SOUND_PROCESSOR_METHOD = os.environ.get('SOUND_PROCESSOR_METHOD', 'HISTGRAM')

MAX_RETRIES = 3

SPEECH_CUT_THRESHOLD = 0.5
SPEECH_MAX_VIDEO_LENGTH = 60 * 5

PID_FILE = path.join(PROJECT_ROOT, 'tmp/video_processor.pid')

USE_SPEECH_RECOGNITION = False
