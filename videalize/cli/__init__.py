import signal

from videalize.worker import worker
from videalize.logger import logger

class CLI:
    def __init__(self):
        self.worker = worker.Worker()

    def run(self):
        signal.signal(signal.SIGINT, self.handler)
        try:
            self.worker.work()
        except KeyboardInterrupt:
            self.handler(signal.SIGINT, None)

    def handler(self, _signum, _frame):
        self.worker.stop()
        logger.info('process interrupted, halting gratefully')
