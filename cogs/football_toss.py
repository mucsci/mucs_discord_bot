import discord
from discord.ext import commands
from discord import app_commands
from utils.fileresource import FileBackedResource
from utils.constants import Constants


class FootballTossCog(commands.Cog):
    PRIVILEGED_THROWERS = {Constants.ADMIN_ROLE_ID, Constants.MOD_ROLE_ID}

    limit = 5
    bot: commands.Bot
    store: FileBackedResource

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.store = FileBackedResource(".football")

    def _action_verb(self, action: str) -> str:
        if action == "toss":
            return "tosses"
        return "throws"

    def _name_for(self, count: int) -> str:
        return (
            "FootballHolder"
            if count == 1
            else f"FootballHolder{min(self.limit, count)}"
        )

    async def _get_role(
        self, interaction: discord.Interaction, count: int
    ) -> discord.Role:
        return discord.utils.get(interaction.guild.roles, name=self._name_for(count))

    async def _get_count(
        self, interaction: discord.Interaction, user: discord.Member
    ) -> int:
        user_roles = user.roles
        football_roles = [
            discord.utils.get(interaction.guild.roles, name=self._name_for(count))
            for count in range(1, self.limit + 1)
        ]
        for role in user_roles:
            try:
                return 1 + football_roles.index(role)
            except:
                pass
        return 0

    async def _update_status(self):
        throws = await self.store.get("total_throws", 0)
        fails = await self.store.get("total_fails", 0)
        activity = discord.Game(name=f"Toss (throws: {throws}, fails: {fails})")
        await self.bot.change_presence(status=discord.Status.idle, activity=activity)
        return

    @app_commands.command(name="throw", description="Throw something to another user")
    async def throw(
        self,
        interaction: discord.Interaction,
        receiver: discord.Member,
        item: str = ":football:",
    ):
        await self.do_throw(interaction, receiver, item, "throw")

    @app_commands.command(name="toss", description="Toss something to another user")
    async def toss(
        self,
        interaction: discord.Interaction,
        receiver: discord.Member,
        item: str = ":football:",
    ):
        await self.do_throw(interaction, receiver, item, "toss")

    async def do_throw(
        self,
        interaction: discord.Interaction,
        receiver: discord.Member,
        item: str,
        action: str,
    ):
        async def add_one(n):
            await self.store.set(n, await self.store.get(n, 0) + 1)

        async def add_role(user, c):
            if 1 <= c:
                await user.add_roles(await self._get_role(interaction, c))

        async def remove_role(user, c):
            if 1 <= c:
                await user.remove_roles(await self._get_role(interaction, c))

        if interaction.channel.name != "footballtoss":
            await interaction.response.send_message(
                "You must be in the #footballtoss channel", delete_after=30.0
            )
            return

        verb = self._action_verb(action)
        thrower = interaction.user
        count = await self._get_count(interaction, thrower)
        if thrower.top_role.id not in self.PRIVILEGED_THROWERS and count == 0:
            await interaction.response.send_message(
                f"{thrower.mention} can't {action} something they don't have"
            )
            await add_one("total_fails")
        else:
            if thrower.top_role.id not in self.PRIVILEGED_THROWERS:
                await remove_role(thrower, count)
                await add_role(thrower, count - 1)
            if receiver.bot:
                await interaction.response.send_message(
                    f"{thrower.mention} just tried to {action} something at a bot"
                )
                await add_one("total_fails")
            else:
                count = await self._get_count(interaction, receiver)
                if receiver.top_role.id not in self.PRIVILEGED_THROWERS:
                    await remove_role(receiver, count)
                    await add_role(receiver, count + 1)
                await interaction.response.send_message(
                    f"{thrower.mention} {verb} a {item} at {receiver.mention}"
                )
                await add_one("total_throws")
        await self._update_status()


async def setup(bot):
    await bot.add_cog(
        FootballTossCog(bot), guilds=[discord.Object(id=Constants.GUILD_ID)]
    )
