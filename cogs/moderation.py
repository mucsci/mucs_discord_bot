import discord
from discord.ext import commands

class ModerationCog(commands.Cog):
    def _init_(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
	    await ctx.channel.purge(limit=amount)

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.send(f'You have been kicked from the MUCS server because {reason}')
        await member.kick(reason = reason)

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await member.send(f'You have been banned from the MUCS server because {reason}')

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, member):
	    banned_users = await ctx.guild.bans()
	    member_name, member_discriminator = member.split('#')

	    for ban_entry in banned_users:
		    user = ban_entry.user

		    if(user.name, user.discriminator) == (member_name, member_discriminator):
			    await ctx.guild.unban(user)
			    await ctx.send(f'Unbanned {user.mention}')
			    return

def setup(bot):
     bot.add_cog(ModerationCog(bot))
