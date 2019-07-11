import os
from datetime import datetime


def unique_directory(directory_name):
    now = datetime.now()
    date = now.strftime("_%d.%m.%Y %H.%M.%S")
    return directory_name + date


def create_directory(directory):
    """Create a directory, if it doesn't exist, in the current working directory to store the various files of keywords.

    Args:
        directory: specified directory name to create in cwd.
    """
    if not os.path.isdir(directory):
        os.mkdir(directory)
