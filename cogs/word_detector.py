import discord
from discord.ext import commands
import asyncio

class WordDetectorCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.lock = asyncio.Lock()
		self.filename = '.wordfilter'
	
	@commands.Cog.listener()
<<<<<<< HEAD
	async def on_message(self, message):
		async with self.lock:
			with open(self.filename, 'r') as readfile:
				words = [line.strip() for line in readfile.readlines()]
			for w in words:
				if w.lower() in message.content.lower():
					await message.delete()
					if not message.author.bot:
						await message.author.send('Illegal word, message deleted', delete_after=30.0)
=======
	async def on_message(self, message): 
		if message.author.bot or str(message.author.top_role) == 'admins':
			return
		async with self.lock:
			words = open(self.filename, 'r')
			for w in words.readlines():
				if w.strip() in message.content.lower():
					await message.delete()
					if w == ':b:' or w == ':regional_indicator_b:':
						await message.author.send('lol', delete_after=10.0)
					else:
						await message.author.send('Illegal word, message deleted', delete_after=10.0)
>>>>>>> 92aa3f77c5fa66479596554753277262a2e9957f
					return
	
	@commands.command(
		name = 'addfilter',
		description = 'Add a word that messages should not contain. (Command is for admins only)',
		usage='addfilter <word1> [<word2>] ...'
	)
	async def addfilter(self, ctx, *words):
<<<<<<< HEAD
		found_duplicate = False
		if str(ctx.author.top_role) != 'admins':
			await ctx.author.send('This command is for admins only', delete_after=30.0)
			return
		async with self.lock:
			with open(self.filename, 'r') as readfile:
				lines = [line.strip() for line in readfile.readlines()]
=======
		await ctx.message.delete()
		if str(ctx.author.top_role) != 'admins':
			await ctx.author.send('This command is for admins only', delete_after=10.0)
			return
		async with self.lock:
			with open(self.filename, 'r') as readfile:
				lines = readfile.readlines()
>>>>>>> 92aa3f77c5fa66479596554753277262a2e9957f
			with open(self.filename, 'a') as appendfile:
				for word in words:
					if word not in lines:
						appendfile.write(word + '\n')
<<<<<<< HEAD
					else:
						await ctx.author.send('Duplicate word not added to filter')
						found_duplicate = True
		if not found_duplicate:
			await ctx.message.delete()

=======
>>>>>>> 92aa3f77c5fa66479596554753277262a2e9957f

	@commands.command(
		name = 'removefilter',
		description = 'Remove a word from the current filter (Command is for admins only)',
		usage='removefilter <word1> [<word2>] ...'
	)
	async def removefilter(self, ctx, *words):
		await ctx.message.delete()
		if str(ctx.author.top_role) != 'admins':
<<<<<<< HEAD
			await ctx.author.send('This command is for admins only', delete_after=30.0)
			return
		async with self.lock:
			with open(self.filename, 'r') as readfile:
				lines = [line.strip() for line in readfile.readlines()]
			with open(self.filename, 'w') as writefile:
				for line in lines:
					if line not in words:
=======
			await ctx.author.send('This command is for admins only', delete_after=10.0)
			return
		async with self.lock:
			with open(self.filename, 'r') as readfile:
				lines = readfile.readlines()
			with open(self.filename, 'w') as writefile:
				for line in lines:
					if line.strip() not in words:
>>>>>>> 92aa3f77c5fa66479596554753277262a2e9957f
						writefile.write(line + '\n')

def setup(bot):
	bot.add_cog(WordDetectorCog(bot))
