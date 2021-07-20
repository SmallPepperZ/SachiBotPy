from customfunctions import config, set_config
import discord 

def save_status(self):
	set_config('status', [list(self.bot_member.activity.type)[1], str(self.bot_member.activity.name), list(self.bot_member.status)[0]], "list")

async def apply_status(bot:discord.Client):
	status = config('status')
	await bot.change_presence(activity=discord.Activity(type=status[0], name=status[1]), status=status[2])

async def changestatus(self, status_type): #pylint:disable=unused-argument
	if self.bot_member.activity is not None:
		await self.bot.change_presence(activity=discord.Activity(type=self.bot_member.activity.type, name=self.bot_member.activity.name), status=status_type)
	else:
		await self.bot.change_presence(status=status_type)
	save_status(self)