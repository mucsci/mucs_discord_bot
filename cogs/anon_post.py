import discord
from discord.ext import commands
from discord import app_commands
from utils.constants import Constants

class AnonPostCog(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@app_commands.command(
		name='anon',
		description='Anonymously post to a course channel',
	)
	async def anon(self, interaction: discord.Interaction, message: str):
		try:
			_ = int(str(interaction.channel.name))
			interaction.user = self.bot.user
			await interaction.response.send_message("Posted anonymously", delete_after=15.0, ephemeral=True)
			await interaction.channel.send('**[anonymous post]** ' + message)
		except:
			await interaction.response.send_message("You can only post anonymously in course channels", delete_after=15.0, ephemeral=True)

async def setup(bot):
	await bot.add_cog(AnonPostCog(bot), guilds=[discord.Object(id=Constants.GUILD_ID)])
