import tempfile
from os import path
import shutil
import requests

from videalize import settings
from videalize.logger import logger
from videalize.processor import Processor
from videalize.worker import file_manager

THUMBNAIL_FILENAME = 'thumbnail.jpg'
PROCESSED_FILENAME = 'processed.mp4'

class ProcessVideoTask:
    def __init__(self):
        self.processor = None
        self.working_dir = None
        self.video = None
        self.feedback_metadata = None

    def run(self, video, feedback_metadata):
        self.video = video
        self.feedback_metadata = feedback_metadata
        video_path = self.fetch_video()
        self.processor = Processor(video_path)
        self.initialize_processing()

        processed_path = path.join(self.working_dir, PROCESSED_FILENAME)
        self.processor.process_video(processed_path)
        self.finalize_processing(processed_path)

        self.cleanup()

    def finalize_processing(self, processed_path):
        file_manager.upload_file(processed_path, self.processed_upload_url)
        payload = {
            'processed_metadata': {
                'duration': self.processor.output_video_length,
            },
            'processed': self.processed_upload_url,
            'status': 'done'
        }
        self.send_feedback(payload)

    def initialize_processing(self):
        thumbnail_path = path.join(self.working_dir, THUMBNAIL_FILENAME)
        self.processor.generate_thumbnail(thumbnail_path)
        file_manager.upload_file(thumbnail_path, self.thumbnail_upload_url)
        logger.debug('uploaded thumbnail to %s', self.thumbnail_upload_url)
        payload = {
            'raw_metadata': {
                'duration': self.processor.video_length,
            },
            'thumbnail': self.thumbnail_upload_url,
            'status': 'processing',
        }
        self.send_feedback(payload)

    def send_feedback(self, payload):
        r = requests.patch(self.feedback_url, json=payload)
        if r.status_code >= 400:
            raise requests.HTTPError('could not send feedback: {0}', r.text)
        else:
            logger.info('updated video %d status to %s', self.video['id'], payload['status'])


    @property
    def feedback_url(self):
        return self.feedback_metadata['feedback_url']

    @property
    def thumbnail_upload_url(self):
        return self.feedback_metadata['thumbnail_upload_url']

    @property
    def processed_upload_url(self):
        return self.feedback_metadata['processed_upload_url']

    def fetch_video(self):
        self.working_dir = tempfile.mkdtemp(prefix=settings.APP_NAME)
        source = self.video['raw']
        destination = path.join(self.working_dir, path.basename(source))
        file_manager.download_file(source, destination)
        logger.debug('file downloaded to %s', destination)
        return destination

    def notify_failure(self, error):
        payload = {
            'status': 'failed',
            'status_details': str(error)
        }
        requests.patch(self.feedback_url, json=payload)

    def cleanup(self):
        shutil.rmtree(self.working_dir)
