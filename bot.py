import discord
from discord.ext import commands
import random
import os

description = '''the MUCS Discord Bot'''

if __name__ == '__main__':
	bot = commands.Bot(command_prefix='!')
	bot.load_extension('cogs.football_toss')
	bot.load_extension('cogs.emote_reactor')
	bot.run(os.environ['DISCORD_TOKEN'])
