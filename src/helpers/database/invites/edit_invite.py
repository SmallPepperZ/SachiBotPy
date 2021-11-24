

from pony.orm.core import ObjectNotFound, db_session
from .invitee import Invitee

def get_invitee(user_id:int):
    try:
        return Invitee[str(user_id)]
    except ObjectNotFound as error:
            raise KeyError(f"No invitee found for {user_id}") from error

@db_session
def edit_invitee(user_id, *_, invite_message_id=None, invite_state=None, status=None, status_editor=None, username=None, level=None, message_count=None, mention=None, info=None, inviter_id=None):
    user = get_invitee(user_id)
    for arg in edit_invitee.__kwdefaults__:
        value = locals()[arg]
        if value is not None:
            setattr(user, arg, value)
