import discord
from discord import emoji
from discord.commands import permissions
from discord.commands.commands import slash_command
from discord.commands.permissions import permission
from discord.ext import commands
from discord.ext.commands import Bot
from discord.commands import message_command, Option
from discord.commands.context import ApplicationContext
from discord.ext.commands.errors import BadArgument



reactions = {
    "Yes and No": ["<:yes:836795924977549362>", "<:no:836795924633354332>"],
    "Up and Down": ["<:upvote:771082566752665681>", "<:downvote:771082566651609089>"],
    "Check and Cross": ["<:yes:786997173845622824>","<:no:786997173820588073>"],
    "Shrug": ["🤷"],
}
number_emojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]

class ReactionCommand(commands.Cog):
    def __init__(self, bot:Bot):
        self.bot = bot




    @slash_command(name="react", guild_ids=[797308956162392094], description='Reacts to a message', default_permission=False)
    @permissions.is_owner()
    async def react(self, ctx:ApplicationContext,
        message:Option(str, "The message link of the message to react to"), 
        emoji_set:Option(str, "The emojis to react with", choices=reactions.keys(), required=False),
        numbers:Option(int, "The number of numbers to react with", choices=range(1,11), required=False)):
        
        try:
            message:discord.Message = await commands.converter.MessageConverter().convert(ctx, str(message))
        except BadArgument:
            await ctx.respond("Could not find message", ephemeral=True)
            return

        if emoji_set is None and numbers is None:
            emojis = message.reactions

        elif emoji_set is None and numbers is not None:
            if numbers <= 10 and numbers >= 1:
                emojis = number_emojis[:numbers]
            else:
                await ctx.respond("Must specify an emoji set or a number between 1 and 10, inclusive", ephemeral=True)
                return

        elif emoji_set is not None and numbers is None:
            emojis = reactions[emoji_set]

        else:
            await ctx.respond("Only specify a set or a number, not both", ephemeral=True)
            return

        await ctx.defer(ephemeral=True)

        for emoji in emojis:
            await message.add_reaction(emoji)
        
        await ctx.respond(f"Reacted", ephemeral=True)
        return






def setup(bot):
    bot.add_cog(ReactionCommand(bot))