from pony.orm.core import ObjectNotFound, db_session
from .entry import Config
from . import dump_type

def set_config_key(key:str, value):
    pass

@db_session
def set_config(**kwargs):
    for key, value in kwargs.items():
        try:
            config_item = Config[key]
            config_item.value = dump_type(value)
        except ObjectNotFound as error:
            raise KeyError(f"No config item found for key '{key}'") from error