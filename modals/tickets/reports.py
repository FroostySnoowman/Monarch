import discord
import yaml

from buttons.tickets.ticketclose import TicketClose

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = data["Tickets"]["PLAYER_REPORT_EMBED_COLOR"]
ticket_category_id = data["Tickets"]["TICKET_CATEGORY_ID"]

class PlayerReports(discord.ui.Modal, title='Player Reports'):

    name = discord.ui.TextInput(
        label='What is your in-game name?',
        placeholder='Type your in-game name here...',
        max_length=50,
        style=discord.TextStyle.short,
    )

    rulebreaker = discord.ui.TextInput(
        label="What is the rule-breaker's in-game name?",
        placeholder="Type the rule breaker's in-game name here...",
        max_length=50,
        style=discord.TextStyle.short,
    )

    reason = discord.ui.TextInput(
        label='What is the reason for the report?',
        placeholder='Type the reason here...',
        max_length=2000,
        style=discord.TextStyle.paragraph,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(content='The ticket is being created...', ephemeral=True)

        category_channel = interaction.guild.get_channel(ticket_category_id)
        ticket_channel = await category_channel.create_text_channel(
            f"report-{interaction.user.name}")
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

        view = TicketClose()

        embed=discord.Embed(title="Responses", 
        description=f"""
**Name**: {self.name.value}

**Rule-Breaker**: {self.rulebreaker.value}

**Reason**: {self.reason.value}
""", 
        color=discord.Color.from_str(embed_color))
        embed.set_footer(text="Please provide evidence of the rule-breaker!")

        await ticket_channel.send(content=x, embed=embed, view=view)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        print(error)