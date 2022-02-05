import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.commands import slash_command, Option
from discord.commands.context import ApplicationContext

from helpers.database.logs.log_channels import LogChannel, db_session
from datetime import timedelta




class InviteCreateListener(commands.Cog):
    def __init__(self, bot:Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_invite_create(self, invite:discord.Invite):
        print("invite created")
        with db_session: channel:discord.TextChannel = LogChannel[str(invite.guild.id)].get_invite_channel(self.bot)
        embed = discord.Embed(title='Invite Created', color=0x2BDE1F, description=f"""
        **Guild**
        ID       : `{invite.guild.id}`
        Name     : [{invite.guild.name}](https://discord.com/channels/{invite.guild.id})
        **Channel**
        ID       : `{invite.channel.id}`
        Name     : [{invite.channel.name}](https://discord.com/channels/{invite.guild.id}/{invite.channel.id})
        Mention  : {invite.channel.mention}
        **Inviter**
        ID       : `{invite.inviter.id}`
        Name     : {invite.inviter}
        Mention  : {invite.inviter.mention}
        **Other**
        Max Time : `{str(timedelta(seconds=invite.max_age))}`
        Max Uses : `{invite.max_uses}`
        Code     : `{invite.code}`
        """)
        await channel.send(embed=embed, content=f"`{invite.guild.name}` invite created by `{invite.inviter}`")

    @commands.Cog.listener("on_invite_delete")
    async def invite_create(self, invite:discord.Invite):
        with db_session: channel:discord.TextChannel = LogChannel[str(invite.guild.id)].get_invite_channel(self.bot)
        embed = discord.Embed(title='Invite Deleted', color=0xD9361C, description=f"""
        **Guild**
        ID       : `{invite.guild.id}`
        Name     : [{invite.guild.name}](https://discord.com/channels/{invite.guild.id})
        **Channel**
        ID       : `{invite.channel.id}`
        Name     : [{invite.channel.name}](https://discord.com/channels/{invite.guild.id}/{invite.channel.id})
        Mention  : {invite.channel.mention}
        **Other**
        Code     : `{invite.code}`
        """)
        await channel.send(embed=embed, content=f"`{invite.guild.name}` invite deleted")





def setup(bot):
    bot.add_cog(InviteCreateListener(bot))