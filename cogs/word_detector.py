import discord
from discord.ext import commands
from utils.fileresource import FileBackedResource
import asyncio

class WordDetectorCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.lock = asyncio.Lock()
		self.filename = '.wordfilter'
	
	@commands.Cog.listener()
	async def on_message(self, message): 
		if message.author.bot or str(message.author.top_role) == 'admins':
			return
		async with self.lock:
			words = open(self.filename, 'r')
			for w in words.readlines():
				if w.strip() in message.content.lower():
					await message.delete()
					if w == ':b:' or w == ':regional_indicator_b':
						await message.author.send('lol', delete_after=10.0)
					else:
						await message.author.send('Illegal word, message deleted', delete_after=10.0)
					return
	
	@commands.command(
		name = 'addfilter',
		description = 'Add a word that messages should not contain. (Command is for admins only)',
		usage='addfilter <word1> [<word2>] ...'
	)
	async def addfilter(self, ctx, *words):
		await ctx.message.delete()
		if str(ctx.author.top_role) != 'admins':
			await ctx.author.send('This command is for admins only', delete_after=10.0)
			return
		async with self.lock:
			with open(self.filename, 'r') as readfile:
				lines = readfile.readlines()
			with open(self.filename, 'a') as appendfile:
				for word in words:
					if word not in lines:
						appendfile.write(word + '\n')

	@commands.command(
		name = 'removefilter',
		description = 'Remove a word from the current filter (Command is for admins only)',
		usage='removefilter <word1> [<word2>] ...'
	)
	async def removefilter(self, ctx, *words):
		await ctx.message.delete()
		if str(ctx.author.top_role) != 'admins':
			await ctx.author.send('This command is for admins only', delete_after=10.0)
			return
		async with self.lock:
			with open(self.filename, 'r') as readfile:
				lines = readfile.readlines()
			with open(self.filename, 'w') as writefile:
				for line in lines:
					if line.strip() not in words:
						writefile.write(line + '\n')

def setup(bot):
	bot.add_cog(WordDetectorCog(bot))
