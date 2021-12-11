import json

def load_type(item) -> "str|int|dict|list":
        if item.type == "string":
            return str(item.value)
        if item.type == "list":
            return json.loads(item.value)
        if item.type == "hex":
            int_version = int(item.value, 16)
            if hex(int_version) == item.value:
                return int_version
            else:
                return int(item.value)
        else:
            raise ValueError("Invalid config type")

def dump_type(value, type) -> "str":
    if type in ("string","int"):
        return str(value)
    if type in ("list","dict"):
        return json.dumps(value)
    if type in ("hex",):
        return hex(value)
    else:
        raise ValueError("Invalid config type")