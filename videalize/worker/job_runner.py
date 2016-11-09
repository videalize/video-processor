import tempfile
from os import path

from videalize import settings
from videalize.logger import logger
from . import file_manager

KNOWN_TASKS = ['process_video']

class JobRunner:
    def __init__(self):
        pass

    def run_job(self, job):
        return getattr(self, job['task'])(job)

    def process_video(self, job):
        [video] = job['args']
        self.fetch_video(video)

    def fetch_video(self, video):
        tempdir = tempfile.mkdtemp(prefix=settings.APP_NAME)
        source = video['raw']
        destination = path.join(tempdir, path.basename(source))
        file_manager.download_file(source, destination)
        logger.debug('file downloaded to %s', destination)
        return destination
