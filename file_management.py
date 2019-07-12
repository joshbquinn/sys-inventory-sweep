from datetime import datetime
import json


def time_stamp():
    now = datetime.now()
    date = now.strftime("%d.%m.%Y %Hhr.%Mm.%Ss")
    return dict({'Date': date})


def write_json_file(filename, json_dict):
    """Write items from a list to a specified file if the items do not already exist in the file.
        Add the url string to the top of the file for source address.

    Args:
        items: A list to write to a file
        file_name: The specified file name to write the list to.
        url_string: The URL the list of words has been created from.

    """
    with open(filename, 'a+') as f:
        json.dump(json_dict, f)

    f.close()

