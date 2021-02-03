import asyncio
import discord
emojis = {"✅": True, "❎": False}

async def confirm(self:discord.ext.commands.Cog, ctx:discord.ext.commands.Context, msg:discord.Message, *args, timeout:int=20) -> bool or None:
	"""Waits for confirmation via reaction from the user before continuing

	Parameters
	----------
	self : discord.ext.commands.Cog
		Cog the command is invoked in

	ctx : discord.ext.commands.Context
		Command invocation context

	msg : discord.Message
		The message to prompt for confirmation on

	timeout = timeout : int, optional
		How long to wait before timing out (seconds), by default 20

	Returns
	-------
	output : bool or None
		True if user confirms action, False if user does not confirm action, None if confirmation times out
	
	
	"""
	for emoji in emojis.keys():
		await msg.add_reaction(emoji)
	try:
		reaction, user = await self.bot.wait_for(
			'reaction_add',
			check=lambda r, u: (r.message.id == msg.id) and (u.id == ctx.author.id) and (r.emoji in emojis),
			timeout=timeout
			)
		if emojis[reaction.emoji] == True:
			return True
		else:
			return False
	except asyncio.TimeoutError:
		return None
	finally:
		await msg.clear_reactions()