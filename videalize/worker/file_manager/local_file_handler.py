import shutil
import os

def download_file(source, destination):
    shutil.copyfile(source, destination)

def upload_file(source, destination):
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    shutil.copyfile(source, destination)
