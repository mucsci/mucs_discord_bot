import discord
from discord.ext import commands

class EmoteReactorCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	lookup = {
		'a': ['🇦', '🅰️', 'ª'],
		'b': ['🇧', '🅱️', 'ℬ'],
		'c': ['🇨', '℃', '©'],
		'd': ['🇩'],
		'e': ['🇪'],
		'f': ['🇫', '℉'],
		'g': ['🇬', 'ℊ'],
		'h': ['🇭', 'ℌ'],
		'i': ['🇮', 'ℹ️', 'ℹ︎'],
		'j': ['🇯'],
		'k': ['🇰'],
		'l': ['🇱'],
		'm': ['🇲', 'Ⓜ️', 'ℳ'],
		'n': ['🇳'],
		'o': ['🇴', '🅾️', 'º'],
		'p': ['🇵', '🅿️', '℗'],
		'q': ['🇶'],
		'r': ['🇷', '℞', '®'],
		's': ['🇸'],
		't': ['🇹'],
		'u': ['🇺'],
		'v': ['🇻'],
		'w': ['🇼'],
		'x': ['🇽'],
		'y': ['🇾'],
		'z': ['🇿'],
		'1': ['1️⃣'],
		'2': ['2️⃣'],
		'3': ['3️⃣'],
		'4': ['4️⃣'],
		'5': ['5️⃣'],
		'6': ['6️⃣'],
		'7': ['7️⃣'],
		'8': ['8️⃣'],
		'9': ['9️⃣'],
		'0': ['0️⃣'],
		}
	
	@commands.command(
		name='emotereact',
		description='Add emote flair to someone\'s post',
		usage='<message id> <string>'
	)
	async def emotereact(self, ctx, message_id: int, react_string: str):
		await ctx.message.delete()
		msg = await ctx.channel.fetch_message(message_id)
		counts = {}
		emotes = []
		try:
			for c in react_string:
				if not c in counts:
					counts[c] = 0
				else:
					counts[c] += 1
				e = EmoteReactorCog.lookup[c][counts[c]]
				emotes.append(e)
			for e in emotes:
				await msg.add_reaction(e)
		except:
			await ctx.author.send("the reaction string cannot be represented using the characters specified", delete_after=30.0)
		return

def setup(bot):
	bot.add_cog(EmoteReactorCog(bot))
