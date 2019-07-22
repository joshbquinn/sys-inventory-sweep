#!/usr/bin/env python

import json


def write_json_file(filename, json_dict):
    """Write key:value pairs from a dictionary to a specified file.

    Args:
        filename: A name to specify a file to write to (or create if doesn't exist)
        json_dict: a dictionary to convert to json and write to file
    """
    # json pretty print
    with open(filename, 'a+') as f:
        json.dump(json_dict, f)

    f.close()

