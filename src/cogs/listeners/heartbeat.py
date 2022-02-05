from discord.ext import commands, tasks
from discord.ext.commands import Bot

import requests

from helpers import config


class HeartbeatCommand(commands.Cog):
    def __init__(self, bot:Bot):
        self.bot = bot
        self.send_heartbeat.start()

    @tasks.loop(minutes=10)
    async def send_heartbeat(self):
        requests.get(config.heartbeat)


def setup(bot):
    bot.add_cog(HeartbeatCommand(bot))
