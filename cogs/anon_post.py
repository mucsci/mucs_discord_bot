import discord
from discord.ext import commands

class AnonPostCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(
		name='anon',
		description='Anonymously post to a permitted channel',
		usage='<message>'
	)
	async def anon(self, ctx):
		try:
			room = int(str(ctx.channel))
			msg = ctx.message.clean_content
			msg = msg.replace('!anon', '**[anonymous post]**', 1)
			await ctx.send(msg)
			await ctx.message.delete()
		except:
			await ctx.author.send("You can only post anonymously in course rooms", delete_after=30.0)

async def setup(bot):
	await bot.add_cog(AnonPostCog(bot))
