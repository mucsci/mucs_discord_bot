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
		await ctx.message.delete()
		await ctx.author.send("The Cyber Defense Organization is an educational and interactive environment tailored toward students with an affinity toward working with computers, servers, firewalls and many other devices/services to defend cyber networks!\n\nInterested in joining? Become a member by joining Get Involved here: https://getinvolved.millersville.edu/organization/cdo\n\nAlso, join our Teams channel here: https://teams.microsoft.com/l/team/19%3a68dc34386f3546c081d120428e6c202c%40thread.skype/conversations?groupId=a38cbcda-b6e1-4417-8804-32a8a9ecca5e&tenantId=92ec3794-b8f0-4f93-b733-7a30a8a2b51b\n\nYou can reach out to any of the members and officers either on this discord or on Teams!")


	@commands.command(
		name='CDOlinks',
		description='Links to cdo social',
		usage='CODlinks'
	)
	async def links(self, ctx): 
		await ctx.message.delete()
		await ctx.author.send("Become a member by joining Get Involved here: https://getinvolved.millersville.edu/organization/cdo\n\nAlso, join our Teams channel here: https://teams.microsoft.com/l/team/19%3a68dc34386f3546c081d120428e6c202c%40thread.skype/conversations?groupId=a38cbcda-b6e1-4417-8804-32a8a9ecca5e&tenantId=92ec3794-b8f0-4f93-b733-7a30a8a2b51b\n\nYou can reach out to any of the members and officers either on this discord or on Teams!")



	@commands.command(
		name='CDOintro',
		description='Info for new members.',
		usage='CDOintro'
	)
	async def intro(self, ctx): 
		await ctx.message.delete()
		await ctx.author.send("Welcome! Getting started you should go through Bandit: Over the Wire. This will get you comfortable with the linux commmand line.\n\nThe game is located here: https://overthewire.org/wargames/bandit/bandit0.html\n\nAnd if you get stuck here is a guide to help you out: https://medium.com/@Kan1shka9/overthewire-wargames-bandit-walkthrough-df2b86826c67\n\nThe next thing you should do is get a virtual linux machine running on your computer. If you don't know what a virtual machine is check out this video: https://www.youtube.com/watch?v=yIVXjl4SwVo\n\nChoosing which operating system you want to work with is up to you. But I would recommend Ubuntu for people who are just learning linux, and Kali for those who are more advanced.\n\nGetting started with Ubuntu: https://itsfoss.com/install-linux-in-virtualbox/\n\nGetting started with Kali: https://www.nakivo.com/blog/how-to-install-kali-linux-on-virtualbox/\n\nOnce you have one of these installed it will make solving complex problems in future CTFs easier.")

	@commands.command(
		name='CDOprojects',
		description='Projects for new members.',
		usage='CDOprojects'
	)
	async def projects(self, ctx): 
		await ctx.message.delete()
		await ctx.author.send("While our club looks to learn and develop over the semesters, we should also look to informing other people who may not be in our club!\nAn important aspect of this interest and possible profession, is that we take the information we learn and apply it to helping others undertstand what security is. \nI have found or come up with some simple projects to get you started if maybe you have been lost. \n\n- Create a phishing email \nThis isn't the most exciting task, but draft an email that has a link to a non-existant website and then send it to your friends and family! \nMake the email not seem like a bot sent it to them, and then if they click the link, they might ask why it didn't work. Let them know about the dangers of clicking on random links sent to them\nas email is one of the easiest ways to break into someones machine and steal EVERYTHING. \n\n- Try using Wireshark\nWireshark is a packet sniffer and analysis tool that captures network traffic on a local network and stores the data for offline analysis. \nthis website is a great tutorial to get you into this fantastic tool: https://www.varonis.com/blog/how-to-use-wireshark/\nWireshark comes on Kali Linux so get a kali vm up and running and you're good to go. \n\n- Create a small script \nWrite a basic script using a scripting language such as Bash, PowerShell, Python, etc, to create a local user account on a computer and set permissions as you see fit. \nBut make sure this is done in a script that can be executable through a shell on whatever box you want. \n(Scripting is easier than you think and is an excellent tool)\nhttps://www.geeksforgeeks.org/introduction-to-scripting-languages/\n\nIf you complete these and like the stuff you did, I highly recommend checking out this website to tackle some harder challenges and really build a foundational knowledge in the field. https://cybercademy.org/\nEnjoy!!")
	
	
	@commands.Cog.listener()
	async def on_message(self, message): 
		if message.author.bot:
			return	 
		if "todd" in message.content.lower():
			await message.channel.send("Happy Birthday Todd!!!!!")
		if "nasa" in message.content.lower():
			await message.channel.send("https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Great_tit_side-on.jpg/1200px-Great_tit_side-on.jpg")


def setup(bot):
	bot.add_cog(CDOBotCog(bot))
