import discord
import yaml
from discord import app_commands
from discord.ext import commands

from buttons.tickets.ticketsystem import TicketSystem

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]

class TicketsCog(commands.GroupCog, name="tickets"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 

    @app_commands.command(name="panel", description="Sends the ticket panel.")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.default_permissions(administrator=True)
    async def panel(self, interaction: discord.Interaction):
        view = TicketSystem()
        embed = discord.Embed(title="Support Tickets",
            description="Click the button that corresponds to your issue below!",
            color=discord.Color.from_str(embed_color))
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message('Sent!', ephemeral=True)

async def setup(bot):
    await bot.add_cog(TicketsCog(bot), guilds=[discord.Object(id=guild_id)])