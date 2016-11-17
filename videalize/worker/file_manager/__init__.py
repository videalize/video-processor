from urllib.parse import urlparse

from . import local_file_handler
from . import s3_file_handler

def download_file(source, destination):
    parsed = urlparse(source)
    if parsed.scheme == 'file':
        return local_file_handler.download_file(parsed.path, destination)
    elif parsed.scheme == 's3':
        return s3_file_handler.download_file(parsed.netloc, parsed.path, destination)
    else:
        raise ValueError('no available handler for scheme {0}'.format(parsed.scheme))

def upload_file(source, destination):
    parsed = urlparse(destination)
    if parsed.scheme == 'file':
        return local_file_handler.upload_file(source, parsed.path)
    elif parsed.scheme == 's3':
        return s3_file_handler.upload_file(source, parsed.netloc, parsed.path)
    else:
        raise ValueError('no available handler for scheme {0}'.format(parsed.scheme))
