from pony.orm.core import ERDiagramError, PrimaryKey, Required, select
from .. import db
import json

try:
    class Config(db.Entity):
        key = PrimaryKey(str)
        value = Required(str)
        type = Required(str)
    db.generate_mapping(create_tables=True)
    
except ERDiagramError:
    pass


