from collections import Counter
import discord
from discord.ext import commands
from discord import Message, app_commands
from utils.constants import Constants
from discord import ui

EMOTE_LOOKUP = {
    "a": ["", "'"],
    "b": ["", "'"],
    "c": [""],
    "d": [""],
    "e": [""],
    "f": [""],
    "g": [""],
    "h": [""],
    "i": ["", "'ℹ"],
    "j": [""],
    "k": [""],
    "l": [""],
    "m": ["", "'Ⓜ"],
    "n": [""],
    "o": ["", "'"],
    "p": ["", "'"],
    "q": [""],
    "r": [""],
    "s": [""],
    "t": [""],
    "u": [""],
    "v": [""],
    "w": [""],
    "x": [""],
    "y": [""],
    "z": [""],
    "1": ["1️⃣"],
    "2": ["2️⃣"],
    "3": ["3️⃣"],
    "4": ["4️⃣"],
    "5": ["5️⃣"],
    "6": ["6️⃣"],
    "7": ["7️⃣"],
    "8": ["8️⃣"],
    "9": ["9️⃣"],
    "0": ["0️⃣"],
}


class ReactorString(ui.Modal, title="Emote Reactor"):
    reactor = ui.TextInput(label="Reaction")

    def __init__(self, message: Message):
        super().__init__()
        self.message = message

    async def on_submit(self, interaction: discord.Interaction):
        counts = Counter()
        emotes = []
        try:
            for c in self.reactor.value:
                counts[c] += 1
                emotes.append(EMOTE_LOOKUP[c][counts[c]])
            reactions = [self.message.add_reaction(e) for e in emotes]
            await interaction.response.send_message(
                "Successfully added emote reaction",
                silent=True,
                delete_after=5.0,
                ephemeral=True,
            )
            for r in reactions:
                await r
        except Exception as e:
            await interaction.response.send_message(
                f"the reaction string cannot be represented using the characters specified",
                delete_after=15.0,
                ephemeral=True,
            )


class EmoteReact(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name="Emote React",
            callback=self.emote_react,
            guild_ids=[Constants.GUILD_ID],
        )
        self.bot.tree.add_command(self.ctx_menu, override=True)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    async def emote_react(
        self, interaction: discord.Interaction, message: discord.Message
    ):
        await interaction.response.send_modal(ReactorString(message))


async def setup(bot: commands.Bot):
    await bot.add_cog(EmoteReact(bot))
    
