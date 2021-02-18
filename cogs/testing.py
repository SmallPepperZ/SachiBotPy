import discord
from discord.ext import commands
import json
import os
from disputils import BotEmbedPaginator
from customfunctions import EmbedMaker
import keyring

#region Variable Stuff


embedcolor = int(keyring.get_password("SachiBotPY", "embedcolor"), 16)

#endregion
import sqlite3
db_path = "storage/SachiBotStorage.db"
dbcon = sqlite3.connect(str(db_path))
dbcur = dbcon.cursor()

class TestingCog(commands.Cog, name="Testing"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def testcommand(self, ctx, *, content):
		embed = discord.Embed(title="hi")
		EmbedMaker.add_description_field(embed, "Key", "Value", boldkey=False)
		await ctx.reply(embed=embed)	
	
	@commands.command()
	@commands.cooldown(rate=1, per=300)
	@commands.check(commands.is_owner())
	async def changeinvitehelp(self, ctx, *, contents):
		channel = self.bot.get_channel(792558439863681046)
		message = await channel.fetch_message(804147923285573633)
		embed=discord.Embed(color=embedcolor, description=contents)
		await message.edit(embed=embed)
		


	@commands.command()
	@commands.check(commands.is_owner())
	async def errorme(self, ctx):
		await ctx.reply(1/0)

	@commands.command(aliases=['tos'])
	async def siren(self, ctx, *, content:str=None):
		if not content:
			await ctx.reply("Give me something to say!")
		else:
			await ctx.message.delete()
			embed = discord.Embed(title="<a:WeeWooRed:771082566874169394>  "+content+"  <a:WeeWooRed:771082566874169394>", color=0xf21b1b )
			await ctx.send(embed=embed)

		

	@commands.command()
	async def commandlistold(self, ctx):
		#logging.info(self.get_commands())
		
		commands = [cmd.name for cmd in self.get_commands()]
		
		delim = ", "
		command_list = delim.join(list(map(str, commands)))
		await ctx.reply(command_list)
		

		
	@commands.group()
	async def newexport(self, ctx):
		if ctx.invoked_subcommand is None:
			delim=", "
			subcommands = [cmd.name for cmd in ctx.command.commands]
			await ctx.send(f'Please select one of the subcommands ({delim.join(list(map(str, subcommands)))})')
	
	@newexport.command()
	async def channel(self, ctx, channelid: str):
		await ctx.send(f'Exporting channel {channelid}...')

	@newexport.command()
	async def guild(self, ctx, guild_id: str):
		await ctx.send(f'Exporting Guild {guild_id}...')

	@commands.command()
	@commands.check(commands.is_owner())
	async def convertinvitees(self, ctx):
		inviteesdict = {
				"archive": {
					"denied": {
						"337267679465570305": 811078965753413682,
						"560551797760983055": 811078968508809250,
						"549770240532152320": 811078972405317632,
						"316508111240429568": 811078977854504992
					},
					"approved": {
						"592377749457469444": 804146859739971594,
						"287372868814372885": 805541148541976626,
						"778102342750437408": 806638169227001886,
						"485500438964076546": 808495238518800484
					}
				},
				"active": {
					"640730699544002571": 804057883964342302,
					"769710557904240721": 804058738780536872,
					"716522494378508368": 804059095275143169,
					"596502366740807702": 804059169862713414,
					"97797564866236416": 804059259415429145,
					"636698104594169856": 804059341027803198,
					"720812649348071554": 804060048015097927,
					"685302220362743849": 804060151807737906,
					"764534820843421737": 804060207495250004,
					"638706588722528256": 806596397314867200,
					"554728508790931477": 806944313342820373,
					"643269075396591626": 806961960896954400,
					"349852668812066817": 807260966445121597,
					"718461587236716584": 808394833508827157,
					"530361907283099650": 809809568829407262
				},
				"testing": {
					"685302220362743849": 804060151807737906
				}
			}
		for userid in inviteesdict["active"].keys():
			messageid = inviteesdict["active"][userid]




def setup(bot):
    bot.add_cog(TestingCog(bot))


"""
user_id              = user_info[0]
invite_message_id    = user_info[1]
invite_activity_type = user_info[2]
field_status         = user_info[3]
field_status_editor  = user_info[4]
field_username       = user_info[5]
field_level          = user_info[6]
field_messages       = user_info[7]
field_mention        = user_info[8]
field_info           = user_info[9]
field_inviter_id     = user_info[10]
"""