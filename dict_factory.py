import re
from itertools import zip_longest


def two_column_dict(category_name, a_list):

    a_dict = {}
    i = 1

    if isinstance(a_list, dict):
        a_dict[category_name] = a_list
        return a_dict
    else:
        zipped = zip(a_list[::2], a_list[1::2])
        a_dict[category_name] = dict(zipped)
        return a_dict


def multiple_column_dict(category_name, a_string):

    result = {}
    header = None
    c = 1
    for line in a_string.splitlines():
        line = line.strip().split()
        if not header:
            header = line
        else:
            key = category_name.format(c)
            result.update({key: dict(zip_longest(header, line, fillvalue=""))})
            c += 1

    return result


def clean_list(a_list):
    delimiters = "\n", ":"
    regex_pattern = '|'.join(map(re.escape, delimiters))
    a_string = re.split(regex_pattern, str(a_list))
    return list(a_string)



































