import discord
from discord.ext import commands
from discord.commands import slash_command

import time, datetime
from helpers import config

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot:discord.Client = bot

    @slash_command(guild_ids=[], description="Gets the bot's uptime and latency")
    async def ping(self, ctx:discord.ApplicationContext):
        current_time = time.time()
        difference   = int(round(current_time - ctx.bot.start_time))
        uptime       = str(datetime.timedelta(seconds=difference))
        embed        = discord.Embed(color=config.embedcolor)
        embed.add_field(name="Ping", value=f'🏓 Pong! {round(self.bot.latency * 1000)}ms', inline='false')
        embed.add_field(name="Uptime", value=f'{uptime}')
        embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar.url)
        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(PingCommand(bot))
