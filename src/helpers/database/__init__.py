from pony.orm import Database

db = Database()
db.bind(provider="sqlite", filename="../../storage/SachiBotStorage.db", create_db=False)


from .config.config import Config
from .invites.invitee import Invitee

db.generate_mapping(create_tables=True)

from .get_config import config

from .invites.edit_invite import edit_invitee
