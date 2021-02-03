import discord
from discord.ext import commands
import json
import random
import os

#region Variable Stuff

with open('storage/config.json', 'r') as file:
	configfile = file.read()

configjson = json.loads(configfile)
embedcolor = int(configjson["embedcolor"], 16)
#endregion



class FunCog(commands.Cog, name="Fun"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=['repeat'])
	async def simonsays(self, ctx, *, content:str=None):
		if not content:
			await ctx.reply("Give me something to say!")
		else:
			if ctx.message.author.id != 545463550802395146: 
				m1 = ":| You can't push me around like that"
				m2 = "You literally typed 11 extra characters to try and get me to do something for you"
				m3 = "Um, no thanks"
				m4 = "I'd reallly rather not say that"
				m5 = "Just say it yourself"
				m6 = "C'mon, just... just remove '%simonsays' and it works"
				m7 = "I am not your speech bot"
				m8 = "You aren't paying me, so no thanks"
				m9 = "I don't work for free"
				m10 = "Make your own simonsays bot"
				m11 = str(ctx.author.mention)+" asked me politely to say "+content
				m12 = "I've always wanted to be a simon"
				msg = random.choice([m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12])
				await ctx.reply(str(msg))
			else:
				await ctx.message.delete()
				await ctx.send(content)

	@commands.command(aliases=['repeatembed'])
	async def simonsaysembed(self, ctx, *, content:str=None):
		if not content:
			await ctx.reply("Give me something to say!")
		else:
			if ctx.message.author.id != 545463550802395146: 
				m1 = ":| You can't push me around like that"
				m2 = "You literally typed 11 extra characters to try and get me to do something for you"
				m3 = "Um, no thanks"
				m4 = "I'd reallly rather not say that"
				m5 = "Just say it yourself"
				m6 = "C'mon, just... just remove '%simonsays' and it works"
				m7 = "I am not your speech bot"
				m8 = "You aren't paying me, so no thanks"
				m9 = "I don't work for free"
				m10 = "Make your own simonsays bot"
				m11 = str(ctx.author.mention)+" asked me politely to say "+content
				m12 = "I've always wanted to be a simon"
				msg = random.choice([m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12])
				#embed = discord.Embed(description=str(msg))
				await ctx.reply(str(msg))
			else:
				await ctx.message.delete()
				embed=discord.Embed(color=embedcolor, description=content)
				await ctx.send(embed=embed)


	@commands.command(aliases=['factoid'])
	async def fact(self, ctx):

		fact = os.popen('curl -s -X GET "https://uselessfacts.jsph.pl/random.txt?language=en" | grep ">" | sed s/\>\ //g').read()
		embed = discord.Embed(color=embedcolor, title="Fact:", description=fact)
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)

		await ctx.reply(embed=embed)

	
	@commands.command()
	async def advice(self, ctx):

		api = os.popen('curl -sX GET https://api.adviceslip.com/advice').read()
		apijson = json.loads(api)
		advice = apijson["slip"]["advice"]
		embed = discord.Embed(title="Advice", color=embedcolor, description=advice)
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
		await ctx.reply(embed=embed)
		
	@commands.command(aliases=['kitty', 'kitten'])
	async def cat(self, ctx):
		catapi = os.popen('curl -s https://api.thecatapi.com/v1/images/search').read()
		catjson = json.loads(catapi)
		caturl = catjson[0]["url"]
		embed = discord.Embed(title="Dog", color=embedcolor)
		embed.set_image(url=caturl)
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
		await ctx.reply(embed=embed)

	@commands.command(aliases=['doggo', 'puppy'])
	async def dog(self, ctx):
		dogapi = os.popen('curl -s https://api.thedogapi.com/v1/images/search').read()
		dogjson = json.loads(dogapi)
		dogurl = dogjson[0]["url"]
		embed = discord.Embed(title="Cat", color=embedcolor)
		embed.set_image(url=dogurl)
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
		await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(FunCog(bot))