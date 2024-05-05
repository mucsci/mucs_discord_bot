import discord
from discord.ext import commands
from discord import app_commands
from utils.constants import Constants

class AnonPostCog(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@app_commands.command(
		name='anon',
		description='Anonymously post to a supported channel',
	)
	async def anon(self, interaction: discord.Interaction, message: str):
		try:
			category_name = interaction.channel.category.name.lower()
		except:
			category_name = None
		CATEGORIES = ["subjects", "csci courses", "language help", "resources", "help"]
		if category_name in CATEGORIES:
			await interaction.response.send_message("Posted anonymously", delete_after=15.0, ephemeral=True)
			mod_channel = await self.bot.fetch_channel(Constants.MOD_ONLY_CHANNEL_ID)
			await interaction.channel.send('**[anonymous]** ' + message)
			await mod_channel.send(f"{interaction.user.name} sent an anonymous message in {interaction.channel.name}: {message}")
		else:
			await interaction.response.send_message(f"You can only post anonymously in the following categories: {', '.join(CATEGORIES)}", delete_after=15.0, ephemeral=True)

async def setup(bot):
	await bot.add_cog(AnonPostCog(bot), guilds=[discord.Object(id=Constants.GUILD_ID)])
