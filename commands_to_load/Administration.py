from discord.ext import commands
import discord
from main import commandFolder
import subprocess

import logging
logger = logging.getLogger('wall_e')

class Administration():

	def __init__(self, bot):
		self.bot = bot

	async def botManager(self, ctx):
		return ctx.message.author in discord.utils.get(ctx.guild.roles, name="Bot_manager").members

	@commands.command()
	async def load(self, ctx, name):
		logger.info("[Administration load()] load command detected from "+str(ctx.message.author))
		if await self.botManager(ctx):
			try:
				logger.info("[Administration load()] "+str(ctx.message.author)+" successfully authenticated")
				self.bot.load_extension(commandFolder+name)
				await ctx.send("{} command loaded.".format(name))
				logger.info("[Administration load()] "+name+" has been successfully loaded")
			except(AttributeError, ImportError) as e:
				await ctx.send("command load failed: {}, {}".format(type(e), str(e)))
				logger.error("[Administration load()] loading "+name+" failed :"+str(type(e)) +", "+ str(e))
		else:
			logger.error("[Administration load()] unauthorized command attempt detected from "+ ctx.message.author)
			await ctx.send("You do not have adequate permission to execute this command, incident will be reported")

	@commands.command()
	async def unload(self, ctx, name):
		logger.info("[Administration unload()] unload command detected from "+str(ctx.message.author))
		if await self.botManager(ctx):
			logger.info("[Administration unload()] "+str(ctx.message.author)+" successfully authenticated")
			self.bot.unload_extension(commandFolder+name)
			await ctx.send("{} command unloaded".format(name))
			logger.info("[Administration unload()] "+name+" has been successfully loaded")
		else:
			logger.error("[Administration unload()] unauthorized command attempt detected from "+ ctx.message.author)
			await ctx.send("You do not have adequate permission to execute this command, incident will be reported")

	@commands.command()
	async def reload(self, ctx, name):
		logger.info("[Administration reload()] reload command detected from "+str(ctx.message.author))
		if await self.botManager(ctx):
			logger.info("[Administration reload()] "+str(ctx.message.author)+" successfully authenticated")
			self.bot.unload_extension(commandFolder+name)
			try:
				self.bot.load_extension(commandFolder + name)
				await ctx.send("`{} command reloaded`".format(commandFolder+name))
				logger.info("[Administration reload()] "+name+" has been successfully reloaded")
			except(AttributeError, ImportError) as e:
				await ctx.send("Command load failed: {}, {}".format(type(e), str(e)))
				logger.error("[Administration load()] loading "+name+" failed :"+str(type(e)) +", "+ str(e))

		else:
			logger.error("[Administration reload()] unauthorized command attempt detected from "+ ctx.message.author)
			await ctx.send("You do not have adequate permission to execute this command, incident will be reported")

	@commands.command()
	async def exc(self, ctx, *args):
		logger.info("[Administration exc()] exc command detected from "+str(ctx.message.author) + "with arguments \""+" ".join(args)+"\"")
		if await self.botManager(ctx):
			logger.info("[Administration exc()] "+str(ctx.message.author)+" successfully authenticated")
			query = " ".join(args)
			await ctx.send("```"+subprocess.getoutput(query)+"```")
		else:
			logger.error("[Administration exc()] unauthorized command attempt detected from "+ str(ctx.message.author))
			await ctx.send("You do not have adequate permission to execute this command, incident will be reported")



def setup(bot):
	bot.add_cog(Administration(bot))