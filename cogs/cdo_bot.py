import discord
from discord.ext import commands
from utils.fileresource import FileBackedResource


class CDOBotCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		name='CDOinfo',
		description='info about CDO',
		usage='CDOinfo'
	)
	async def info(self, ctx): 
		await ctx.send("The Cyber Defense Organization is an educational and interactive environment tailored toward students with an affinity toward working with computers, servers, firewalls and many other devices/services to defend cyber networks!\n\nInterested in joining? Become a member by joining Get Involved here: https://getinvolved.millersville.edu/organization/cdo\n\nAlso, join our Teams channel here: https://teams.microsoft.com/l/team/19%3a68dc34386f3546c081d120428e6c202c%40thread.skype/conversations?groupId=a38cbcda-b6e1-4417-8804-32a8a9ecca5e&tenantId=92ec3794-b8f0-4f93-b733-7a30a8a2b51b\n\nYou can reach out to any of the members and officers either on this discord or on Teams!")


	@commands.command(
		name='CDOlinks',
		description='Links to cdo social',
		usage='CODlinks'
	)
	async def links(self, ctx): 
		await ctx.send("Become a member by joining Get Involved here: https://getinvolved.millersville.edu/organization/cdo\n\nAlso, join our Teams channel here: https://teams.microsoft.com/l/team/19%3a68dc34386f3546c081d120428e6c202c%40thread.skype/conversations?groupId=a38cbcda-b6e1-4417-8804-32a8a9ecca5e&tenantId=92ec3794-b8f0-4f93-b733-7a30a8a2b51b\n\nYou can reach out to any of the members and officers either on this discord or on Teams!")



	@commands.command(
		name='CDOnewmember',
		description='Info for new members.',
		usage='CDOnewmember'
	)
	async def newmember(self, ctx): 
		await ctx.send("Welcome! Getting started you should go through Bandit: Over the Wire. This will get you comfortable with the linux commmand line.\n\nThe game is located here: https://overthewire.org/wargames/bandit/bandit0.html\n\nAnd if you get stuck here is a guide to help you out: https://medium.com/@Kan1shka9/overthewire-wargames-bandit-walkthrough-df2b86826c67\n\nThe next thing you should do is get a virtual linux machine running on your computer. If you don't know what a virtual machine is check out this video: https://www.youtube.com/watch?v=yIVXjl4SwVo\n\nChoosing which operating system you want to work with is up to you. But I would recommend Ubuntu for people who are just learning linux, and Kali for those who are more advanced.\n\nGetting started with Ubuntu: https://itsfoss.com/install-linux-in-virtualbox/\n\nGetting started with Kali: https://www.nakivo.com/blog/how-to-install-kali-linux-on-virtualbox/\n\nOnce you have one of these installed it will make solving complex problems in future CTFs easier.")
	
	@commands.Cog.listener()
	async def on_message(self, message): 
		if message.author.bot:
			return	 
		if "todd" in message.content.lower():
			await message.channel.send("Happy Birthday Todd!!!!!")

def setup(bot):
	bot.add_cog(CDOBotCog(bot))
