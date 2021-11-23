from pony.orm.core import select
import json

from .entry import Config

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


class __ConfigData():
    discordtoken:str
    embedcolor:int
    enabledguilds:list[int]
    errorchannel:int
    errornum:int
    githubgist:str
    githubtoken: str
    heartbeat:str
    pathtohide:str
    prefix:str
    status:list[int, str]
    
    def __init__(self):
        config_items = select(c for c in Config)
        for item in config_items:
            setattr(self, item.key, load_type(item))


    


config = __ConfigData()