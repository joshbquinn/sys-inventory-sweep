import platform
import json



if platform.system() == 'Windows':
    os_in_use = 'Windows'
elif platform.system() == 'Linux':
    os_in_use = 'Linux'


def djs(dictionary_object):
    return json.dumps(dictionary_object, indent=4)


def write_json_file(filename, json_list):

    with open(filename, 'a+') as f:
        json.dump(json_list, f)


def write_to_file(file_name, items):
    """Write items from a list to a specified file if the items do not already exist in the file.
    Add the url string to the top of the file for source address.

    Args:
        items: A list to write to a file
        file_name: The specified file name to write the list to.
        url_string: The URL the list of words has been created from.

    """

    f = open(file_name, 'a+', encoding='utf-8')

    f.write(f'{os_in_use} System Inventory List: ' + date + '\n\n')

    for item in items:
        f.write(item)
    f.close()

