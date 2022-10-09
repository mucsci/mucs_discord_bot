import discord
import typing
from discord.ext import commands
from utils.fileresource import FileBackedResource

class FootballTossCog(commands.Cog):

	limit = 5
	
	def __init__(self, bot):
		self.bot = bot
		self.store = FileBackedResource('.football')

	def _name_for(self, x):
		return 'FootballHolder' if x == 1 else f'FootballHolder{min(FootballTossCog.limit,x)}'
		
	async def _get_count(self, ctx, user):
		user_roles = user.roles
		football_roles = [discord.utils.get(ctx.guild.roles, name=self._name_for(count)) for count in range(1,FootballTossCog.limit + 1)]
		for role in user_roles:
			try:
				return 1 + football_roles.index(role)
			except:
				pass
		return 0
	
	async def _get_role(self, ctx, count):
		return discord.utils.get(ctx.guild.roles, name=self._name_for(count))
	
	async def _update_status(self):
		throws = await self.store.get('total_throws', 0)
		fails = await self.store.get('total_fails', 0)
		activity = discord.Game(name="Toss (throws: {}, fails: {})".format(throws, fails))
		await self.bot.change_presence(status=discord.Status.idle, activity=activity)
		return

	@commands.command(
		name='throw',
		description='Throw something to another user',
		aliases=['throws', 'toss'],
		usage='[item=:football:] <mention>'
	)
	async def throw(self, ctx, item : typing.Optional[str] = ":football:", *, receiver: discord.Member):
		async def add_one (n):
			await self.store.set(n, await self.store.get(n, 0) + 1)

		async def add_role (user, c):
			if 1 <= c:
				await user.add_roles(await self._get_role(ctx, c))

		async def remove_role (user, c):
			if 1 <= c:
				await user.remove_roles(await self._get_role(ctx, c))
		
		await ctx.message.delete()
		if str(ctx.channel) != 'footballtoss':
			await ctx.author.send("you must be in the #footballtoss channel", delete_after=30.0)
			return
		thrower = ctx.author
		count = await self._get_count(ctx, thrower)
		action = 'throw'
		admin=736216045857144892
		mod=736216473009258497
		privileged_throwers = [admin, mod]
		if thrower.top_role.id not in privileged_throwers and count == 0:
			await ctx.send(f'{thrower.mention} can\'t {action} something they don\'t have')
			await add_one ('total_fails')
		else:
			if thrower.top_role.id not in privileged_throwers:
				await remove_role(thrower, count)
				await add_role(thrower, count - 1)
			if receiver.bot:
				await ctx.send(f'{thrower.mention} just tried to {action} something at a bot')
				await add_one ('total_fails')
			else:
				count = await self._get_count(ctx, receiver)
				if receiver.top_role.id not in privileged_throwers:
					await remove_role(receiver, count)
					await add_role(receiver, count + 1)
				await ctx.send(f'{thrower.mention} {action}s a {item} at {receiver.mention}')
				await add_one ('total_throws')
		await self._update_status()
		return


def setup(bot):
	bot.add_cog(FootballTossCog(bot))
