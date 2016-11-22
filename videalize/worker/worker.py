import json

from videalize import settings
from videalize.logger import logger
from .subscriber import RedisSubscriber
from .errors import InvalidJobError
from . import tasks

JOB_REQUIRED_KEYS = ['args', 'jid', 'task']

class Worker:
    def __init__(self, subscriber=None):
        self.running = False
        if subscriber is None:
            subscriber = RedisSubscriber()
        self.subscriber = subscriber

    def work(self):
        self.running = True
        self.subscriber.start()
        while self.running:
            job = self.subscriber.wait_job()
            if job is not None:
                logger.info('processing job %s', job)
                self.process_raw_job(job)

    def process_raw_job(self, raw_job):
        try:
            job = json.loads(raw_job.decode('utf8'))
            self.validate_job_format(job)
            self.process_job(job, settings.MAX_RETRIES)
            self.subscriber.clear_job(job)
        except json.JSONDecodeError as e:
            logger.error('could not read job: %s', str(e))
        except InvalidJobError as e:
            logger.error('job has an invalid format: %s', str(e))
        except UnicodeDecodeError as e:
            logger.error('job contains invalid unicode: %s', str(e))

    @staticmethod
    def validate_job_format(job):
        for key in JOB_REQUIRED_KEYS:
            if key not in job:
                raise InvalidJobError('job should have key %s', key)

    def process_job(self, job, retries):
        task = tasks.get_runner(job['task'])
        try:
            task.run(*job['args'])
        except (KeyboardInterrupt, SystemExit) as e:
            raise e
        except Exception as e: # pylint: disable=W0703
            self.handle_failure(job, task, retries, e)

    def handle_failure(self, job, task, retries, error):
        logger.warning('could not process job %s: %s', job['jid'], str(error))
        if retries > 0:
            logger.info('retrying to process %s (%d retries left)',
                        job['jid'], retries)
            self.process_job(job, retries - 1)
        else:
            logger.error('job %s failed', job['jid'])
            task.notify_failure(error)

    def stop(self):
        self.running = False
