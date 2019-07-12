import json

def serialize_json(string_object):
    return json.loads(string_object)


def deserialize_json(dictionary_object):
    return json.dumps(dictionary_object, indent=4)