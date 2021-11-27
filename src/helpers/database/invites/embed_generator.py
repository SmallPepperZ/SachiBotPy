import discord
from pony.orm.core import db_session
from .edit_invite import get_invitee
from ...embed.embed_helper import DescriptionEmbed

@db_session
def create_embed(user_id:int):
    user = get_invitee(user_id)
    embed = DescriptionEmbed(color=user.color, description=f'__**{user.user_id}**__')
    embed.add_field("Maincord Level",    user.level)
    embed.add_field("Maincord Messages", user.message_count)
    embed.add_field("Mention",           f"<@{user.user_id}>")
    embed.add_field("User ID",           f'`{user.id}`')
    embed.add_field("Invite Status",     user.status_message)
    embed.add_field("Info",              user.info)
