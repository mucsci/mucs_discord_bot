import discord
from discord.ext import commands

class ModerationCog(commands.Cog):
    def _init_(self, bot):
        self.bot = bot

    @commands.command(
        name = 'clear',
        description = 'Erases messages in the current channel. Default is 5 messages. Must have manage message permission to use.',
        usage = '<numbermessageserase>'
    )
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
	    await ctx.channel.purge(limit=amount)

    @commands.command(
        name = 'kick',
        description = 'kicks a tagged user from the server and sends them a DM with the reason for the kick. Requires kick permission.',
        usage = '<user> <reason>'
    )
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.send(f'You have been kicked from the MUCS server because {reason}')
        await member.kick(reason = reason)

    @commands.command(
        name = 'ban',
        description = 'bans a tagged user from the server and sends them a DM with the reason for the ban. Requires ban permission.',
        usage = '<user> <reason>'
    )
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await member.send(f'You have been banned from the MUCS server because {reason}')

    @commands.command(
        name = 'unban',
        description = 'unbans a tagged user from the server. Requires ban permission to use.',
        usage = '<user> <reason>'
    )
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
