#!/usr/bin/env python

import os
from time_stamper import time_stamp


def unique_directory(directory_name):
    """Create a unique directory name with a timestamp

    Args:
        directory_name: a string parameter to name the the directory
    """
    date = time_stamp()
    return directory_name + date


def create_directory(directory):
    """Create a directory, if it doesn't exist, in the current working directory to store the various files of keywords.

    Args:
        directory: specified directory name to create in cwd.
    """
    if not os.path.isdir(directory):
        os.mkdir(directory)
