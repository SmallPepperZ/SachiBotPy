from typing import Any
from pony.orm.core import db_session, select
import builtins
from .config import Config
from .config.type_conversion import load_type

from .config.set import set_config


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
    
    @db_session
    def __init__(self):
        config_items = select(c for c in Config)
        for item in config_items:
            print(item)
            value = load_type(item)
            print(value)
            super().__setattr__(item.key, value)

    def __setattr__(self, __name: str, __value: Any) -> None:
        set_config(**{__name:__value})
        super().__setattr__(__name, __value)


config = __ConfigData()