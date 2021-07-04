
import random
import os
import requests
import discord
from discord.ext import commands
from customfunctions import del_msg
from customfunctions import config, OBJECTS_TO_BONK_WITH, master_logger


#region Variable Stuff

logger = master_logger.getChild("fun")
embedcolor = config("embedcolor")
#endregion

def simonsays_responses(ctx, content):
	responses = ["You can't push me around like that",
				 "You literally typed 11 extra characters to try and get me to do something for you",
				 "Um, no thanks",
				 "I'd reallly rather not say that",
				 "Just say it yourself",
				 "C'mon, just... just remove '%simonsays' and it works",
				 "I am not your speech bot",
				 "You aren't paying me, so no thanks",
				 "I don't work for free",
				 "Make your own simonsays bot",
				 f"{ctx.author.mention} asked me politely to say {content}",
				 "I've always wanted to be a simon"
				]
	return responses


class FunCog(commands.Cog, name="Fun"):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(aliases=['repeat'])
	async def simonsays(self, ctx, *, content:str=None):
		if not content:
			await ctx.reply("Give me something to say!")
		else:
			if ctx.message.author.id != 545463550802395146:
				responses = simonsays_responses(ctx, content)
				msg = random.choice(responses)
				await ctx.reply(msg)
			else:
				await del_msg(ctx.message)
				await ctx.send(content)

	@commands.command(aliases=['repeatembed'])
	async def simonsaysembed(self, ctx, *, content:str=None):
		if not content:
			await ctx.reply("Give me something to say!")
		else:
			if ctx.message.author.id != 545463550802395146:
				responses = simonsays_responses(ctx, content)
				msg = random.choice(responses)
				#embed = discord.Embed(description=str(msg))
				await ctx.reply(str(msg))
			else:
				await del_msg(ctx.message)
				embed=discord.Embed(color=embedcolor, description=content)
				await ctx.send(embed=embed)


	@commands.command(aliases=['factoid'])
	async def fact(self, ctx):

		fact = os.popen('curl -s -X GET "https://uselessfacts.jsph.pl/random.txt?language=en" | grep ">" | sed s/> //g').read()
		embed = discord.Embed(color=embedcolor, title="Fact:", description=fact)
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)

		await ctx.reply(embed=embed)

	@commands.command(aliases=['quotes'])
	async def quote(self, ctx):
		response = requests.get('https://api.quotable.io/random').json()
		text = response['content']
		author = response["author"]
		embed = discord.Embed(color=embedcolor, description=f'>>> {text}')
		embed.set_author(name=author)
		embed.set_footer(text=f"Request by {ctx.author} | api: api.quotable.io/random", icon_url= ctx.author.avatar_url)
		await ctx.reply(embed=embed)



	@commands.command()
	async def advice(self, ctx):

		apijson = requests.get('https://api.adviceslip.com/advice').json()
		advice = apijson["slip"]["advice"]
		embed = discord.Embed(title="Advice", color=embedcolor, description=advice)
		embed.set_footer(text=f"Request by {ctx.author} | api: api.adviceslip.com/advice", icon_url= ctx.author.avatar_url)
		await ctx.reply(embed=embed)

	@commands.command(aliases=['kitty', 'kitten'])
	async def cat(self, ctx):
		catjson = requests.get('https://api.thecatapi.com/v1/images/search').json()
		caturl = catjson[0]["url"]
		embed = discord.Embed(title="Dog", color=embedcolor)
		embed.set_image(url=caturl)
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
		await ctx.reply(embed=embed)

	@commands.command(aliases=['doggo', 'puppy'])
	async def dog(self, ctx):
		dogjson = requests.get('https://api.thedogapi.com/v1/images/search').json()
		dogurl = dogjson[0]["url"]
		embed = discord.Embed(title="Cat", color=embedcolor)
		embed.set_image(url=dogurl)
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
		await ctx.reply(embed=embed)

	@commands.command(aliases=['tos'])
	@commands.is_owner()
	async def siren(self, ctx, *content):
		if not content:
			await ctx.reply("Give me something to say!")
		else:
			content = ' '.join(content)
			await del_msg(ctx.message)
			embed = discord.Embed(title="<a:WeeWooRed:771082566874169394>  " +
								  content+"  <a:WeeWooRed:771082566874169394>", color=0xf21b1b)
			await ctx.send(embed=embed)

	@commands.command()
	async def ban(self, ctx, user:discord.Member, *, reason:str=None):
		try:
			await del_msg(ctx.message)
		except discord.errors.Forbidden:
			pass
		quantity = random.randint(1,100000)
		if quantity>1:
			item = random.choice(OBJECTS_TO_BONK_WITH)[1]
		else:
			item = random.choice(OBJECTS_TO_BONK_WITH)[0]

		if reason is None:
			await ctx.send(embed=discord.Embed(color=embedcolor,description=f"{user.mention} was banned by {ctx.author.mention} for {quantity} {item}"))
		else:
			await ctx.send(embed=discord.Embed(color=embedcolor,description=f"{user.mention} was banned by {ctx.author.mention} for {quantity} {item} because {reason}"))


def setup(bot):
	bot.add_cog(FunCog(bot))
