import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.commands import slash_command, Option
from discord.commands.context import ApplicationContext

class DummyGuild():
    def __init__(self, id:int):
        self.id = id


class BotInviteCommand(commands.Cog):
    def __init__(self, bot:Bot):
        self.bot = bot




    @slash_command(guild_ids=[], description='Creates a bot invite link')
    async def oauth_invite(self, ctx:ApplicationContext, 
            bot:Option(discord.User, "The bot to invite", required=False, default=None), 
            guild:Option(str, "The guild to invite it to", required=False, default=None), 
            slash_scope:Option(bool, "Whether to give the bot the slash command scope", required=False, default=False)):

        bot:Bot = bot or self.bot.user
        if guild is None:
            guild = ctx.guild
        else:
            guild = DummyGuild(int(guild))
        scopes = ('bot','applications.commands') if slash_scope else ('bot',)
        url = discord.utils.oauth_url(client_id=bot.id, guild=guild, scopes=scopes)
        await ctx.respond(url, ephemeral=True)




def setup(bot):
    bot.add_cog(BotInviteCommand(bot))