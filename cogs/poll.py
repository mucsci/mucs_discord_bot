import re
import random
import asyncio
import discord
from discord.ext import commands

class PollCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name = 'pollhelp',
        description = 'Explains how the poll command works.',
        usage=''
    )
    async def pollhelp(self, ctx):
        await ctx.message.delete()
        
        embed = discord.Embed(
            title = 'Poll Help',
            description = 'This command allows you to create a very simple poll.\n' 
                + 'The poll question should be in quotes, followed by your\ncomma seperated choices. '
                + 'The last argument after the | is optional.\nThis allows you to set a time limit (seconds) on your poll.\n'
                + 'The poll has a default time limit of 2 minutes if no time is set.',
            colour = 0x62738d)
        embed.add_field(name='Example Syntax', value='!poll "<question>" <choice1>, <choice2>, .. <choiceN> | <seconds>')

        await ctx.send(embed=embed)

    @commands.command(
        name = 'poll',
        description = 'Creates a simple poll, check out !pollhelp for more details',
        usage = '"<question>" <choice1>, <choice2>, .. <choiceN>'
    )
    async def poll(self, ctx):
        await ctx.message.delete()

        question = re.findall('"([^"]*)', ctx.message.clean_content)
        if not question:
            await ctx.send(f"{ctx.message.author.mention}, for syntax check out !help poll")
            return
        choices = question[1]
        if not choices:
            await ctx.send(f"{ctx.message.author.mention}, for syntax check out !pollhelp")
            return
        if not choices.find('|') == -1:
            choices = choices.split('|')
            self.timer = int(choices[1])
            choices = choices[0]
        else:
            self.timer = 120

        poll_choices = [(chr(0x1f1e6 + i), c) for i, c in enumerate(choices.split(',')[0:])]
        poll_embed = discord.Embed(
            title = "**" + question[0] + "**",
            description = "\n".join(f"{key} : {c}" for key, c in poll_choices),
            colour = 0x83bae3
        )

        poll = await ctx.send(embed=poll_embed)
        for emoji, _ in poll_choices:
            await poll.add_reaction(emoji)

        await asyncio.sleep(self.timer)
        await poll.delete()

def setup(bot):
    bot.add_cog(PollCog(bot))

