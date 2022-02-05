from ntpath import join
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.commands import slash_command, Option
from discord.commands.context import ApplicationContext

from helpers.database.logs.log_channels import LogChannel, db_session
from datetime import timedelta

from helpers import config
from helpers.embed.embed_helper import DescriptionEmbed
from pony.orm.core import ObjectNotFound


class BotJoinListener(commands.Cog):
    def __init__(self, bot:Bot):
        self.bot = bot
        self.log_guild = 909148074260168784


    @commands.Cog.listener("on_guild_join")    
    async def on_guild_join(self, guild: discord.Guild):
        channel = self.bot.get_guild(797308956162392094).get_channel(867605721424199710)

        join_embed = discord.Embed(color=config.embedcolor, title="Added to guild", description=f"""
		**Guild**
		ID       : `{guild.id}`
		Name     : [{guild.name}](https://discord.com/channels/{guild.id})
		Owner    : {guild.owner.mention}({guild.owner})""")

        owner_in_server = discord.utils.get(
            guild.members, id=self.bot.owner.id) is not None
        
        join_embed.add_field(name="Owner in Guild", value=owner_in_server)
        if owner_in_server:
            await channel.send(embed=join_embed)
        else:
            await channel.send(embed=join_embed, content="Leaving server")
            await guild.leave()

        # Create logging channels if they don't exist 
        with db_session:
            try: 
                LogChannel[str(guild.id)]
            except ObjectNotFound:
                log_guild = await self.bot.fetch_guild(self.log_guild)
                guild_category = await log_guild.create_category(name=guild.name, reason=f"Joined {guild.name}")
                invite_channel = await log_guild.create_text_channel(name=f'invites', topic=f"Invite logging for {guild.name} ({guild.id})", reason=f"Joined {guild.name}", category=guild_category)
                join_channel = await log_guild.create_text_channel(name=f'joins', topic=f"Join logging for {guild.name} ({guild.id})", reason=f"Joined {guild.name}", category=guild_category)

                guild_embed = DescriptionEmbed(
                    title=f"{guild.name}", color=config.embedcolor, description="")
                if guild.icon is not None:
                    guild_embed.set_thumbnail(url=guild.icon.url)
                guild_embed.add_field("ID", f"`{guild.id}`")
                guild_embed.add_field("Name", f"[{guild.name}](https://discord.com/channels/{guild.id})")
                guild_embed.add_field("Owner", f"{guild.owner}")

                LogChannel(guild_id=str(guild.id), log_category=str(guild_category.id), join_channel=str(join_channel.id), invite_channel=str(invite_channel.id))

    @commands.Cog.listener("on_guild_remove")
    async def on_guild_remove(self, guild: discord.Guild):

        channel = self.bot.get_guild(797308956162392094).get_channel(867605721424199710)

        join_embed = discord.Embed(color=config.embedcolor, title="Left guild", description=f"""
		**Guild**
		ID       : `{guild.id}`
		Name     : [{guild.name}](https://discord.com/channels/{guild.id})
		Owner    : {guild.owner.mention} ({guild.owner})""")
        await channel.send(embed=join_embed)





def setup(bot):
    bot.add_cog(BotJoinListener(bot))