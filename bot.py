import discord
from discord.ext import commands
import random
import os
import aiohttp
from utils.constants import Constants

description = """the MUCS Discord Bot"""


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(name=f"cogs.{filename[:-3]}")


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(),
            application_id=Constants.APPLICATION_ID,
        )

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        await self.tree.sync(guild=None)
        await self.tree.sync(guild=discord.Object(id=Constants.GUILD_ID))
        await load_extensions()
        synced = await self.tree.sync(guild=discord.Object(id=Constants.GUILD_ID))
        print(f'Synced {len(synced)} commands: [{"] -- [".join(s.name for s in synced)}]')

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_ready(self):
        await self.wait_until_ready()
        print(f"Logged in as {self.user}.")


if __name__ == "__main__":
    bot = Bot()  # Calling the class
    bot.run(os.environ["DISCORD_TOKEN"])
