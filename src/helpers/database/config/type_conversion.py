import json

def load_type(item) -> "str|int|dict|list":
        if item.type == "string":
            return str(item)
        if item.type == "list":
            return json.loads(item.value)
        if item.type == "hex":
            return int(item.value, 16)
        else:
            raise ValueError("Invalid config type")

def dump_type(value) -> "str":
    if type(value) in (str, int):
        return str(value)
    if type(value) == list:
        return json.dumps(value)
    else:
        raise ValueError("Invalid config type")