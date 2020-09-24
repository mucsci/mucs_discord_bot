import discord
from discord.ext import commands
import random
import os

description = '''the MUCS Discord Bot'''

if __name__ == '__main__':
	bot = commands.Bot(command_prefix='!')
	bot.load_extension('cogs.football_toss')
	bot.load_extension('cogs.cdo_bot')
	bot.load_extension('cogs.emote_reactor')
	bot.load_extension('cogs.poll')
	bot.load_extension('cogs.anon_post')
	bot.load_extension('cogs.word_detector')
	bot.run(os.environ['DISCORD_TOKEN'])
