import os
from videalize import settings


def write_pid_file():
    with open(settings.PID_FILE, 'w') as f:
        f.write(str(os.getpid()))


def remove_pid_file():
    try:
        os.remove(settings.PID_FILE)
    except FileNotFoundError:
        pass
