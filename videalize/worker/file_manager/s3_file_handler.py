import sys
import boto

from videalize import settings


def get_connection():
    # NOTE: memoize s3 connection
    if not hasattr(sys.modules[__name__], '_cached_s3_conn'):
        conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID,
                               settings.AWS_SECRET_ACCESS_KEY)
        setattr(sys.modules[__name__], '_cached_s3_conn', conn)
    return getattr(sys.modules[__name__], '_cached_s3_conn')


def download_file(bucket_name, source, destination):
    conn = get_connection()
    bucket = conn.get_bucket(bucket_name)
    file_key = bucket.get_key(source)
    file_key.get_contents_to_filename(destination)


def upload_file(_source, _bucket, _destination):
    raise NotImplementedError
