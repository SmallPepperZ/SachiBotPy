from pony.orm.core import PrimaryKey, Required
from .. import db

class Config(db.Entity):
    _table_ = "config"
    key = PrimaryKey(str)
    value = Required(str)
    type = Required(str)


