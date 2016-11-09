import logging

from . import settings

logger = logging.Logger(settings.APP_NAME)

ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

if settings.ENV == 'dev':
    ch.setLevel(logging.DEBUG)
else:
    ch.setLevel(logging.INFO)

logger.addHandler(ch)
