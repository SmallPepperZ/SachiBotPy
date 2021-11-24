from pony.orm.core import Optional, PrimaryKey, Required
from .. import db
from .terms import get_action


class Invitee(db.Entity):
    _table_ = "invitees"
    user_id             = PrimaryKey(str)
    
    invite_message_id   = Required(str, unique=True)
    invite_state        = Required(str, column="invite_activity_type")
    inviter_id          = Required(str, column="field_inviter_id")

    status              = Required(str, column="field_status")
    status_editor       = Optional(str, column="field_status_editor")
    
    level               = Optional(int, column="field_level")
    message_count       = Optional(int, column="field_messages")
    
    info                = Optional(str, column="field_info")

    @property
    def terms(self):
        return get_action(self.status)

    @property
    def color(self):
        return self.terms.color

    @property
    def status_message(self):
        return self.terms.status_message

    @property
    def confirmation_message(self):
        return self.terms.confirmation_message








