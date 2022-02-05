import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.commands import slash_command, Option
from discord.commands.context import ApplicationContext

from helpers.database.logs.log_channels import LogChannel





class JoinLeaveListener(commands.Cog):
    def __init__(self, bot:Bot):
        self.bot = bot




    @commands.Cog.listener("on_member_join")
    async def member_join(self, member:discord.Member):
        channel:discord.TextChannel = LogChannel[str(member.guild.id)].get_join_channel()
        embed = discord.Embed(title=f'User Joined', color=0x2BDE1F, description=f"""
	    **Guild**
	    ID  : `{member.guild.id}`
	    Name: [{member.guild.name}](https://discord.com/channels/{member.guild.id})
	    **User**
	    ID     : `{member.id}`
	    Name   : {member.name}
	    Mention: {member.mention}
	    """)
        await channel.send(embed=embed, content=f"{member.guild.name} joined by {member}")

    @commands.Cog.listener("on_member_remove")
    async def member_leave(self, member:discord.Member):
        channel:discord.TextChannel = LogChannel[str(member.guild.id)].get_join_channel()
        embed = discord.Embed(title=f'User Left', color=0xD9361C, description=f"""
	    **Guild**
	    ID  : `{member.guild.id}`
	    Name: [{member.guild.name}](https://discord.com/channels/{member.guild.id})
	    **User**
	    ID     : `{member.id}`
	    Name   : {member.name}
	    Mention: {member.mention}
	    """)
        await channel.send(embed=embed, content=f"{member.guild.name} left by {member}")





def setup(bot):
    bot.add_cog(JoinLeaveListener(bot))