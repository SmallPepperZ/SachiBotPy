#pylint:disable=invalid-name
from discord.ext import commands
from discord_slash import cog_ext, SlashContext




modify_options=[
			{
				"name":"appprove",
				"description": "Approves",
				"type": 1,
				"options":	[
								{
									"name": "test",
									"description": "parameter",
									"type": 3
								}
							]
			},
			{
				"name":"deny",
				"description": "Denies",
				"type": 1,
				"options":	[
								{
									"name": "test",
									"description": "parameter",
									"type": 3
								}
							]
			}
]





class Slash(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@cog_ext.cog_slash( name="invite",
						description="Uses the invite features",
						guild_ids=[797308956162392094],
						options=modify_options,
									)
	async def _invite(self, ctx: SlashContext, **args):
		#embed = discord.Embed(title="embed test")
		await ctx.respond()
		await ctx.send_hidden(args)

	@cog_ext.cog_subcommand(base="invite",
							name="add",
							base_description="Commands to work with the invitee system",
							description="Says something",
							guild_ids=[797308956162392094],
							options=[
									{
										"name": "user-id",
										"description": "Who to add to the invitee system",
										"type": 4,
										"required": True
									},
									{
										"name": "info",
										"description": "Any additional info to include in the embed",
										"type": 3,
										"required": False

									},
									{
										"name": "force",
										"description": "Whether to bypass restrictions",
										"type": 5,
										"required": False
									}],
									connector={
										"user-id": "user_id",
										"info": "info",
										"force": "force"
									})
	@commands.command(name="invite_add_test")
	async def _invite_add(self, ctx:SlashContext, user_id:int, info:str=None, force:bool=False, slash_command:bool=True) -> None: #pylint:disable=unused-argument
		await ctx.respond()
		hidden = await ctx.send('hi', hidden=False)
		await hidden.edit(content="Test")
		await ctx.send(f'{force}\n{user_id}\n{info}')

	@cog_ext.cog_subcommand(base="invite",
							name="action",
							description="Performs an action on a user in the invitee system",
							guild_ids=[797308956162392094],
							options=[
									{
										"name": "user-id",
										"description": "Who to edit in the invitee system",
										"type": 4,
										"required": True
									},
									{
										"name": "action",
										"description": "What action to take",
										"type": 3,
										"required": True,
										"choices":	[{
														"name": "Approve    - Moves a user to land",
														"value": "approve",
													},
													{
														"name": "Deny - Queues a user for removal from the system",
														"value": "deny"
													},
													{
														"name": "Accept - Use this if the user accepts the invite and joins",
														"value": "accept"
													},
													{
														"name": "Decline - Use this if the user declines the invite",
														"value": "decline"
													},
													{
														"name": "Pause - Use this to give a user the paused status",
														"value": "pause"
													},
													{
														"name": "Unpause    - Use this to remove a paused status",
														"value": "unpause"
													},
													{
														"name": "Reset      - Sets a user to the default state",
														"value": "reset"
													}
													]

									},
									{
										"name": "force",
										"description": "Whether to bypass restrictions",
										"type": 5,
										"required": False
									}],
									connector={
										"user-id": "user_id",
										"action": "action",
										"force": "force"
									})
	async def _invite_action(self, ctx:SlashContext, user_id:int, action:str=None, force:bool=False) -> None:
		await ctx.respond()
		hidden = await ctx.send('hi', hidden=False)

		await ctx.send(f'{force}\n{user_id}\n{action}')


def setup(bot):
	bot.add_cog(Slash(bot))
