import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.commands import slash_command, Option
from discord.commands.context import ApplicationContext





class SuggestCommand(commands.Cog):
    def __init__(self, bot:Bot):
        self.bot = bot


    @slash_command(guild_ids=[], description='Leave feedback about the bot')
    async def suggest(self, ctx:ApplicationContext, suggestion:Option(str, "Feedback or suggestion you have")):
        suggestion_channel = self.bot.get_channel(801576966952058910)
        embed = discord.Embed(title='', description=suggestion)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        await suggestion_channel.send(embed=embed)
        await ctx.respond("Feedback submitted", ephemeral=True)


def setup(bot):
    bot.add_cog(SuggestCommand(bot))