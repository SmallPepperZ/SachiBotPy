import discord
from discord.commands import Option
from discord.errors import Forbidden
from discord.ext import commands
from discord.ext.commands import Bot
from discord.commands import slash_command


from helpers import config
from helpers.embed.embed_helper import DescriptionEmbed

class WhatisCommand(commands.Cog):
    def __init__(self, bot:Bot):
        self.bot = bot

    @slash_command(guild_ids=[],description="Looks up information for a guild using its widget (often disabled)")
    async def whatis(self, ctx, guild:Option(str, "The ID of the guild to look up")):
        try:
            guild = await self.bot.fetch_widget(int(guild))
        except Forbidden:
            await ctx.respond("This guild does not exist or it does not have its widget enabled", ephemeral=True)
            return
        embed = DescriptionEmbed(title=guild.name, color=config.embedcolor)
        embed.add_field("Creation Time", f"<t:{int(guild.created_at.timestamp())}> (<t:{int(guild.created_at.timestamp())}:R>)")
        if guild.channels is not None:
            embed.add_field("Voice Channels", "\n".join([channel.name for channel in guild.channels]))
        if guild.invite_url is not None:
            embed.add_field("Invite URL", guild.invite_url)
        await ctx.respond(embed=embed)



def setup(bot):
    bot.add_cog(WhatisCommand(bot))