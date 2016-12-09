import sys
import boto
from boto.s3.key import Key

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


def upload_file(source, bucket_name, destination):
    conn = get_connection()
    bucket = conn.get_bucket(bucket_name)
    file_key = Key(bucket)
    file_key.key = destination
    file_key.set_contents_from_filename(source)
