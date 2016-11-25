import json

import redis
from videalize.logger import logger

from videalize import settings

class NotConnectedError(Exception):
    pass


class Subscriber:
    def start(self):
        pass

    def wait_job(self):
        raise NotImplementedError


class RedisSubscriber(Subscriber):
    def __init__(self):
        self.client = None
        self.connected = False

    def start(self):
        logger.info('connecting to redis with url %s', settings.REDIS_URL)
        self.client = redis.from_url(settings.REDIS_URL)
        self.connected = True
        logger.info('starting to listen to queue "%s"', settings.REDIS_PROCESS_VIDEO_QUEUE)

    def wait_job(self):
        if not self.connected:
            raise NotConnectedError('client not connected')

        return self.client.brpoplpush(settings.REDIS_PROCESS_VIDEO_QUEUE,
                                      settings.REDIS_TEMP_VIDEO_QUEUE,
                                      timeout=3)

    def clear_job(self, job):
        popped = []
        while True:
            raw_popped_job = self.client.rpop(settings.REDIS_TEMP_VIDEO_QUEUE)
            if not raw_popped_job:
                break
            popped_job = json.loads(raw_popped_job.decode('utf8'))
            if job['jid'] == popped_job['jid']:
                break
            else:
                popped.append(raw_popped_job)
        if popped:
            self.client.lpush(settings.REDIS_TEMP_VIDEO_QUEUE, *popped)
