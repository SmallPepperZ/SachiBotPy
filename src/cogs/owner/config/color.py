import discord
from discord import permissions
from discord.commands import SlashCommandGroup
from discord.ext import commands
from discord.ext.commands import Bot
from discord.commands import slash_command, Option
from discord.commands.context import ApplicationContext, AutocompleteContext

from helpers.database import config
from helpers.database.config.set import set_config
from helpers import confirmation

from io import BytesIO
from PIL import Image

def create_image(color:str) -> BytesIO:
    color = color.strip("#")
    hexcolor = f"#{color}" # Ensure there is one # at the start of the color
    image    = Image.new("RGB", (100,100), hexcolor)
    buffer   = BytesIO()
    image.save(buffer, "png")
    buffer.seek(0)
    return buffer

class ColorCommand(commands.Cog):    
    def __init__(self, bot:Bot):
        self.bot = bot


    @slash_command(description='Sets the embed color for the ot',default_permission=False, guild_ids=[797308956162392094])
    @permissions.is_owner()
    async def color(self, ctx:ApplicationContext, color:Option(str, "The new embed color")):
        embed = discord.Embed(color=config.embedcolor, title="Embed Color", description = f"Set embed color?")
        color_int = int(color.strip("#"), 16)
        await ctx.defer(ephemeral=True)
        file = discord.File(fp=create_image(color), filename="colorimage.png")
        embed.set_thumbnail(url='attachment://colorimage.png')
        
        msg = await ctx.respond(embed=embed, file=file)

        if await confirmation.confirm(self, ctx, msg, silent=True):
            webhook = ctx.followup
            await webhook.send(embed=discord.Embed(color=color_int, title="Embed Color Set"), ephemeral=True)
            config.embedcolor = color_int





def setup(bot):
    bot.add_cog(ColorCommand(bot))