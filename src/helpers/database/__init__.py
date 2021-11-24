from pony.orm import Database

db = Database()
db.bind(provider="sqlite", filename="../../storage/SachiBotStorage.db", create_db=False)

from .config import config
from .config import set_config