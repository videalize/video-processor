import os
import signal

from videalize import settings
from videalize.worker import worker
from videalize.logger import logger
from videalize.processor import Processor
from . import util

from .parser import cli_parser

class CLI:
    def __init__(self):
        self.worker = worker.Worker()

    def run(self):
        args = cli_parser.parse_args()
        command = args.command or 'listen'
        getattr(self, command)(args)

    def process(self, args):
        processor = Processor(args.video)
        processor.process_video(args.output)

    def listen(self, _args):
        signal.signal(signal.SIGINT, self.handler)
        util.write_pid_file()
        try:
            self.worker.work()
        except KeyboardInterrupt:
            self.handler(signal.SIGINT, None)

    def handler(self, _signum, _frame):
        util.remove_pid_file()
        self.worker.stop()
        logger.info('process interrupted, halting gracefully')
