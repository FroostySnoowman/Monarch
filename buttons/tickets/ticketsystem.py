import discord
import yaml
from discord.ext import commands

from buttons.tickets.applications import ApplicationSystem
from modals.tickets.appeal import PlayerAppeals
from modals.tickets.bug import BugReports
from modals.tickets.general import GeneralSupport
from modals.tickets.other import OtherSupport
from modals.tickets.reports import PlayerReports
from modals.tickets.suggestions import Suggestions

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["Tickets"]["BUG_REPORT_EMBED_COLOR"]
ticket_category_id = data["Tickets"]["TICKET_CATEGORY_ID"]

class TicketSystem(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='🎫', label='General', style=discord.ButtonStyle.grey, custom_id='tickets:1')
    async def general(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(GeneralSupport())

    @discord.ui.button(emoji='🚫', label='Report', style=discord.ButtonStyle.grey, custom_id='tickets:2')
    async def report(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(PlayerReports())

    @discord.ui.button(emoji='🔗', label='Appeal', style=discord.ButtonStyle.grey, custom_id='tickets:3')
    async def appeal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(PlayerAppeals())

    @discord.ui.button(emoji='👑', label='Applications', style=discord.ButtonStyle.grey, custom_id='tickets:4')
    async def applications(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content='The ticket is being created...', ephemeral=True)

        category_channel = interaction.guild.get_channel(ticket_category_id)
        ticket_channel = await category_channel.create_text_channel(
            f"apply-{interaction.user.name}")
        await ticket_channel.set_permissions(interaction.guild.get_role(interaction.guild.id),
            view_channel=False,
            send_messages=False,
            read_messages=False,
            add_reactions=False,
            embed_links=False,
            read_message_history=False,
            external_emojis=False,
            use_application_commands=False)
        
        await ticket_channel.set_permissions(interaction.user,
            send_messages=True,
            read_messages=True,
            add_reactions=True,
            embed_links=True,
            attach_files=True,
            read_message_history=True,
            external_emojis=True,
            use_application_commands=True)

        await interaction.edit_original_response(content=f'The ticket has been created at {ticket_channel.mention}.')

        x = f'{interaction.user.mention}'

        embed=discord.Embed(title="",
        description="Select what you're applying for down below.", 
        color=discord.Color.from_str(embed_color))

        view = ApplicationSystem()

        await ticket_channel.send(content=x, embed=embed, view=view)

    @discord.ui.button(emoji='⚠️', label='Bug Reports', style=discord.ButtonStyle.grey, custom_id='tickets:5')
    async def bugs(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BugReports())

    @discord.ui.button(emoji='🗣️', label='Suggestions', style=discord.ButtonStyle.grey, custom_id='tickets:6')
    async def suggestions(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Suggestions())

    @discord.ui.button(emoji='❔', label='Other', style=discord.ButtonStyle.grey, custom_id='tickets:7')
    async def other(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(OtherSupport())

class TicketSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(TicketSystem())

async def setup(bot):
    await bot.add_cog(TicketSystemCog(bot), guilds=[discord.Object(id=guild_id)])