import discord
from discord.commands.errors import ApplicationCommandInvokeError
from discord.errors import ExtensionFailed, ExtensionNotLoaded
from discord.ext import commands
from discord.ext.commands import Bot
from discord.commands import slash_command, Option
from discord.commands.context import ApplicationContext

from helpers.cogs import pretty_cog_list, pretty_cog_name, format_as_path
from helpers import errors, config
import inspect


async def get_cogs(ctx: discord.AutocompleteContext):
    cogs = [inspect.getmodule(cog).__name__ for cog in ctx.bot.cogs.values()]
    cogs.remove("cogs.cog.reload")
    return pretty_cog_list(cogs)


class ReloadCommand(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(guild_ids=[797308956162392094], description='Reloads cogs')
    async def reload(self, ctx: ApplicationContext, cog: Option(str, "The cog to reload", required=False, autocomplete=get_cogs)):
        if cog is None:
            cogs = [inspect.getmodule(cog).__name__ for cog in self.bot.cogs.values()]
            cogs.remove("cogs.cog.reload")
        else:
            cogs = [format_as_path(cog)]
        cog_entries = []
        for cog in cogs:
            try:
                self.bot.reload_extension(cog)
                cog_entries.append(f'<:Success:865674863330328626> | {pretty_cog_name(cog)}')
            except ExtensionFailed as error:
                cog_entries.append(f'<:Failure:865674863031877663> | {pretty_cog_name(cog)}')
                await errors.report_error(ctx, error, self.bot, silent=True)
            except ExtensionNotLoaded as error:
                await ctx.respond(f"Could not find cog '{cog}'", ephemeral=True)
                return
        embed = discord.Embed(title="Reloaded", description="\n".join(cog_entries), color=config.embedcolor)
        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(ReloadCommand(bot))
