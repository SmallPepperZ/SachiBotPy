
async def command_on_cooldown(ctx, error):
	await ctx.message.add_reaction(str('<:Cooldown:804477347780493313>'))
	if str(error.cooldown.type.name) != "default":
		cooldowntype = f'per {error.cooldown.type.name}'
	else:
		cooldowntype = 'global'
		await ctx.reply(f"This command is on a {round(error.cooldown.per, 0)}s {cooldowntype} cooldown. "
						f"Wait {round(error.retry_after, 1)} seconds",
						delete_after=min(10, error.retry_after))
