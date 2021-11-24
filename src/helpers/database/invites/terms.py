class Term():
    def __init__(self, name, present_participle, status_message, confirmation_message, color):
        self.name = name
        self.present_participle = present_participle
        self.status_message = status_message
        self.confirmation_message = confirmation_message
        self.color = color


def get_action(action):
    terms = {
        "approve": Term("approve", "Approving", "Approved by {status_editor}", "Successfully approved {user}", 0x17820e),
        "deny": Term("deny", "Denying", "Denied by {status_editor}", "Successfully denied {user}", 0xa01116),
        "pause": Term("pause", "Pausing", "Paused by {status_editor}", "Successfully paused {user}", 0x444444),
        "unpause": Term("none", "Unpausing", "None", "Successfully unpaused {user}", 0xFFFF00),
        "reset": Term("none", "Resetting", "None", "Successfully reset {user}'s inviter messsage", 0xFFFF00),
        "accept": Term("accept", "Accepting", "Was invited and joined", "Successfully marked {user} as accepted", 0x1bc912),
        "decline": Term("decline", "Declining", "Was invited but declined", "Successfully marked {user} as declined", 0xd81d1a),
        "none": Term("none", "none", "none", "none", 0xFFFF00)
    }
    try:
        value = terms[action]
    except KeyError as error:
        raise ValueError("Action does not exist") from error
    return value
