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
		with open(self.filename, 'r') as readfile:
			self.words = set(line.strip() for line in readfile.readlines())
	
	async def _add(self, words):
		new_words = set(words)
		with open(self.filename, 'a') as appendFile:
			for w in new_words - self.words:
				appendFile.write(f"{w}\n")
		self.words += new_words
		
	async def _remove(self, words):
		self.words -= set(words)
		with open(self.filename, 'w') as writefile:
			for w in self.words:
				writefile.write (f"{w}\n")
	
	@commands.Cog.listener()
	async def on_message(self, message):
		async with self.lock:
			if message.author.bot:
				return
			ctx = await self.bot.get_context(message)
			special_channel = await self.bot.fetch_channel(self.report_channel_id)
			if ctx.channel == special_channel:
				return
			msg_words = set(message.content.lower().split())
			bad = msg_words & self.words
			if bad:
				list_of_words = ', '.join(bad)
				await message.delete()
				await special_channel.send(f'**{str(ctx.author)} said "{list_of_words}":** {str(ctx.message.content)}')
				await message.author.send(f'Illegal word(s) in message: "{list_of_words}" -- message deleted', delete_after=30.0)
				
	@commands.command(
		name = 'addfilter',
		description = 'Add a word that messages should not contain. (Command is for admins only)',
		usage='addfilter <word1> [<word2>] ...'
	)
	async def addfilter(self, ctx, *words):
		async with self.lock:
			await ctx.message.delete()
			if str(ctx.author.top_role) != 'admins':
				await ctx.author.send('This command is for admins only', delete_after=30.0)
				return
			await self._add(w.lower() for w in words)
		
	@commands.command(
		name = 'removefilter',
		description = 'Remove a word from the current filter (Command is for admins only)',
		usage='removefilter <word1> [<word2>] ...'
	)
	async def removefilter(self, ctx, *words):
		async with self.lock:
			await ctx.message.delete()
			if str(ctx.author.top_role) != 'admins':
				await ctx.author.send('This command is for admins only', delete_after=30.0)
				return
			await self._remove(w.lower() for w in words)

async def setup(bot):
	await bot.add_cog(WordDetectorCog(bot))
