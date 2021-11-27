from datetime import time
from discord.commands import slash_command, Option
from discord.commands.context import ApplicationContext
from discord.errors import NotFound
from discord.ext import commands
from discord.ext.commands import Bot
import discord
from discord import UserFlags

from helpers.embed.embed_helper import DescriptionEmbed


badge_list = {
            UserFlags.staff                    : "<:developer:802021494778626080>",
            UserFlags.partner                  : "<:partneredserverowner:802021495089004544>",
            UserFlags.hypesquad                : "<:hypesquad:802021494925557791>",
            UserFlags.bug_hunter               : "<:bughunterl1:802021561967575040>",
            UserFlags.hypesquad_bravery        : "<:hypesquadbravery:802021495185473556>",
            UserFlags.hypesquad_brilliance     : "<:hypesquadbrilliance:802021495433461810>",
            UserFlags.hypesquad_balance        : "<:hypesquadbalance:802010940698132490>",
            UserFlags.early_supporter          : "<:earlysupporter:802021494989389885>",
            UserFlags.bug_hunter_level_2       : "<:bughunterl2:802021494975889458>",
            UserFlags.verified_bot_developer   : "<:earlybotdeveloper:802021494875488297>"
}

def format_timestamp(timestamp:int) -> str:
    timestamp = int(timestamp)
    return f'<t:{timestamp}> (<t:{timestamp}:R>)'

def get_badges(user:discord.User) -> str:
    try:
        badges = [badge_list[badge] for badge in user.public_flags.all()]
    except KeyError:
        pass
    else:
        if len(badges) > 0:
            return " ".join(list(map(str, badges)))
        else:
            return None

def add_badges(user:discord.User, embed:DescriptionEmbed):
    badges = get_badges(user)
    if badges is not None:
        embed.add_spacer()
        embed.add_field("Badges", badges)

def add_user_details(user:discord.User, embed:DescriptionEmbed) -> None:
        embed.add_field("Mention", user.mention)
        embed.add_field("ID", user.id)
        embed.add_field("Name", f"[{user.display_name}](https://discord.com/users/{user.id})")
        embed.add_spacer()

class WhoisCommand(commands.Cog):
    def __init__(self, bot:Bot):
        self.bot = bot



    def create_user_embed(self, user:discord.User, embed:DescriptionEmbed):
        embed.add_field("Bot", user.bot)

        embed.add_spacer()

        add_user_details(user, embed)

        embed.add_field("Creation Date", format_timestamp(user.created_at.timestamp()))

        add_badges(user, embed)


    def create_member_embed(self, ctx, user:discord.Member, embed:DescriptionEmbed):
        embed.add_field("Bot", user.bot)

        embed.add_field("Server owner", ctx.guild.owner == user)
        embed.add_field("Server admin", user.guild_permissions.administrator)
        embed.add_spacer()

        add_user_details(user, embed)

        embed.add_field("Join Date", format_timestamp(user.joined_at.timestamp()))
        embed.add_field("Creation Date", format_timestamp(user.created_at.timestamp()))

        add_badges(user,embed)

    @slash_command(guild_ids=[797308956162392094], description="Gets information about a user")
    async def whois(self, ctx:ApplicationContext, user:Option(discord.User, "User to query")):
        if isinstance(user, int):
            try:
                user = await self.bot.fetch_user(int(user))
            except NotFound:
                await ctx.respond("User could not be found", ephemeral=True)
                return
        user:discord.User
        
        embed = DescriptionEmbed(color=user.color,title=user)
        embed.set_image(url=user.display_avatar.url)

        if ctx.guild in user.mutual_guilds:
            self.create_member_embed(ctx, user, embed)
        else:
            self.create_user_embed(user, embed)

        await ctx.respond(embed=embed)





def setup(bot):
    bot.add_cog(WhoisCommand(bot))