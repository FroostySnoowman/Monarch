import discord
import yaml
from discord import app_commands
from discord.ext import commands

from buttons.tickets.suggestions import StaffTickets

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

staff_guild_id = data["General"]["STAFF_GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]

class StaffCog(commands.GroupCog, name="staff"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 

    @app_commands.command(name="panel", description="Sends the staff panel.")
    @app_commands.guilds(discord.Object(id=staff_guild_id))
    @app_commands.default_permissions(administrator=True)
    async def panel(self, interaction: discord.Interaction):
        view = StaffTickets()
        embed = discord.Embed(title="Staff Tickets",
            description="""
If you would like to request leave, click the button below fill out the form! Leaves longer than 1 month will require meeting with your Staff Leader. If you wish to make any changes to your leave, submit a new request and notify your Staff Leader.

If you would like to submit a sugggestion, click the button below and fill out the form!
""",
        color=discord.Color.from_str(embed_color))
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message('Sent!', ephemeral=True)

async def setup(bot):
    await bot.add_cog(StaffCog(bot), guilds=[discord.Object(id=staff_guild_id)])