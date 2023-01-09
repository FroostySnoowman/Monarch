import discord
import yaml
from discord.ext import commands

from buttons.tickets.ticketclose import TicketClose

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]

class ApplicationSystem(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='🎮', label='In-Game', style=discord.ButtonStyle.grey, custom_id='application:1')
    async def ingame(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Ingame Staff Applications",
            description="Please apply here: \nhttps://monarchnetwork.xyz/forums/staff-applications.12/",
        color=discord.Color.from_str(embed_color))
        await interaction.response.edit_message(content=interaction.user.mention, embed=embed, view=TicketClose())

    @discord.ui.button(emoji='🆔', label='Discord', style=discord.ButtonStyle.grey, custom_id='application:2')
    async def discords(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Discord Staff Applications",
            description="Please apply here: \nhttps://monarchnetwork.xyz/forums/staff-applications.12/",
        color=discord.Color.from_str(embed_color))
        await interaction.response.edit_message(content=interaction.user.mention, embed=embed, view=TicketClose())

    @discord.ui.button(emoji='🏗️', label='Builder', style=discord.ButtonStyle.grey, custom_id='application:3')
    async def builder(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Builder Applications",
            description="Coming soon...",
        color=discord.Color.from_str(embed_color))
        await interaction.response.edit_message(content=interaction.user.mention, embed=embed, view=TicketClose())

    @discord.ui.button(emoji='📽️', label='YouTube', style=discord.ButtonStyle.grey, custom_id='application:4')
    async def youtube(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="YouTube Applications",
            description="Coming soon...",
        color=discord.Color.from_str(embed_color))
        await interaction.response.edit_message(content=interaction.user.mention, embed=embed, view=TicketClose())

class ApplicationSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(ApplicationSystem())

async def setup(bot):
    await bot.add_cog(ApplicationSystemCog(bot), guilds=[discord.Object(id=guild_id)])