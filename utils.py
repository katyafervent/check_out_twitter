import json


def get_pretty_json_string(dict_to_prettify):
    return json.dumps(dict_to_prettify, indent=4)
