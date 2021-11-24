from pony.orm.core import ObjectNotFound, db_session
from .config import Config
from .type_conversion import dump_type

@db_session
def set_config(**kwargs):
    for key, value in kwargs.items():
        try:
            config_item = Config[key]
            config_item.value = dump_type(value)
        except ObjectNotFound as error:
            raise KeyError(f"No config item found for key '{key}'") from error