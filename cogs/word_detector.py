import discord
from discord.ext import commands
import asyncio
import os

class WordDetectorCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.lock = asyncio.Lock()
		self.filename = '.wordfilter'
		self.report_channel_id = os.environ['DISCORD_WORD_DETECTOR_CHANNEL_ID']
	
	@commands.Cog.listener()
	async def on_message(self, message):
		async with self.lock:
			with open(self.filename, 'r') as readfile:
				words = [line.strip() for line in readfile.readlines()]
			for w in words:
				if w.lower() in ''.join(message.content.lower().split()):
					ctx = await self.bot.get_context(message)
					special_channel = await self.bot.fetch_channel(self.report_channel_id)
					if not message.author.bot:
						await special_channel.send(f'**{str(ctx.author)} said:** {str(ctx.message.content)}')
					if ctx.channel != special_channel:
						await message.delete()
					if not message.author.bot:
						await message.author.send('Illegal word(s), message deleted', delete_after=30.0)
					return
	
	@commands.command(
		name = 'addfilter',
		description = 'Add a word that messages should not contain. (Command is for admins only)',
		usage='addfilter <word1> [<word2>] ...'
	)
	async def addfilter(self, ctx, *words):
		await ctx.message.delete()
		if str(ctx.author.top_role) != 'admins':
			await ctx.author.send('This command is for admins only', delete_after=30.0)
			return
		async with self.lock:
			with open(self.filename, 'r') as readfile:
				lines = [line.strip() for line in readfile.readlines()]
			with open(self.filename, 'a') as appendfile:
				for word in words:
					if word not in lines:
						appendfile.write(word + '\n')
					else:
						await ctx.author.send('Duplicate word not added to filter')

	@commands.command(
		name = 'removefilter',
		description = 'Remove a word from the current filter (Command is for admins only)',
		usage='removefilter <word1> [<word2>] ...'
	)
	async def removefilter(self, ctx, *words):
		if str(ctx.author.top_role) != 'admins':
			await ctx.author.send('This command is for admins only', delete_after=30.0)
			return
		async with self.lock:
			with open(self.filename, 'r') as readfile:
				lines = [line.strip() for line in readfile.readlines()]
			with open(self.filename, 'w') as writefile:
				for line in lines:
					if line not in words:
						writefile.write(line + '\n')
		await ctx.message.delete()
		
def setup(bot):
	bot.add_cog(WordDetectorCog(bot))