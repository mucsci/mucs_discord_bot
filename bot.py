import discord
from discord.ext import commands
import random
import os
import aiohttp 

guild_id = 736215823034744895
description = '''the MUCS Discord Bot'''

# Loading our cogs, iterating through each name in folder named cogs
async def load_extensions(): 
        for filename in os.listdir('./cogs'):
                if filename.endswith(".py"):
                        await bot.load_extension(name=f"cogs.{filename[:-3]}")

class Bot(commands.Bot): # New bot class extending commands.Bot
        def __init__(self): # Initializing bot
                super().__init__(command_prefix='!', intents=discord.Intents.all(), application_id=748146175626182667)

        async def setup_hook(self): # Setup hook for cogs
                self.session = aiohttp.ClientSession() # New aiohttp session
                await load_extensions() # Loading cogs
                await bot.tree.sync(guild=discord.Object(id=guild_id)) #Sync commands

        async def close(self): # Closing the session so it won't error
                await super().close()
                await self.session.close()

        async def on_ready(self): # Inform that it's ready
                await self.wait_until_ready()
                print(f"Logged in as {self.user}.")


if __name__ == '__main__':
        bot = Bot() # Calling the class
        bot.run(os.environ['DISCORD_TOKEN'])
