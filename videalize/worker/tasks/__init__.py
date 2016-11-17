from .process_video import ProcessVideoTask
from ..errors import InvalidJobError

def get_runner(name):
    if name == 'process_video':
        return ProcessVideoTask()
    else:
        raise InvalidJobError('unkonwn task {0}'.format(name))
