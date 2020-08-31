import discord
from discord.ext import commands
from utils.fileresource import FileBackedResource

class FootballTossCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.store = FileBackedResource('.football')
	
	async def _get_role(self, ctx):
		return discord.utils.get(ctx.guild.roles, name='FootballHolder')

	async def _update_status(self):
		activity = discord.Game(name="Toss (throws: {}, fails: {})".format(await self.store.get('total_throws', 0), await self.store.get('total_fails', 0)))
		await self.bot.change_presence(status=discord.Status.idle, activity=activity)
		return

	@commands.command(
		name='throw',
		description='Throw something to another user',
		aliases=['tossfootball','throwfootball','throwball','tossball','footballtoss','footballthrow','ballthrow','balltoss'],
		usage='<mention> [<item>]'
	)
	async def throw(self, ctx, receiver: discord.Member, item=':football:'):
		await ctx.message.delete()
		if str(ctx.channel) != 'footballtoss':
			await ctx.author.send("you must be in the #footballtoss channel", delete_after=30.0)
			return
		role = await self._get_role(ctx)
		thrower = ctx.author
		if not str(thrower.top_role) == 'admins' and not role in thrower.roles:
			await ctx.send(f'{thrower.mention} can\'t throw something they don\'t have')
			await self.store.set('total_fails', await self.store.get('total_fails', 0) + 1)
		else:
			await thrower.remove_roles(role)
			if receiver.bot:
				await ctx.send(f'{thrower.mention} just tried to throw something at a bot')
				await self.store.set('total_fails', await self.store.get('total_fails', 0) + 1)
			else:
				await receiver.add_roles(role)
				await ctx.send(f'{thrower.mention} throws a {item} at {receiver.mention}')
				await self.store.set('total_throws', await self.store.get('total_throws', 0) + 1)
		await self._update_status()
		return


def setup(bot):
	bot.add_cog(FootballTossCog(bot))
