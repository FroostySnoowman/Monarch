import discord
import yaml

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = data["General"]["EMBED_COLOR"]
staff_leave_channel_id = data["Staff"]["STAFF_LEAVE_CHANNEL_ID"]

class StaffLeave(discord.ui.Modal, title='Staff Leave'):

    name = discord.ui.TextInput(
        label='What is your in-game name?',
        placeholder='Type your in-game name here...',
        max_length=50,
        style=discord.TextStyle.short,
    )

    dateleaving = discord.ui.TextInput(
        label="What is the date you're leaving?",
        placeholder="Type the date in mm/dd/yy format here...",
        max_length=100,
        style=discord.TextStyle.short,
    )

    datereturning = discord.ui.TextInput(
        label="What is the date you're returning?",
        placeholder="Type the date in mm/dd/yy format here...",
        max_length=100,
        style=discord.TextStyle.short,
    )

    reason = discord.ui.TextInput(
        label="What is the reason for you leaving?",
        placeholder="Type the reason here...",
        max_length=2000,
        style=discord.TextStyle.paragraph,
    )

    async def on_submit(self, interaction: discord.Interaction):
        staff_leave_channel = interaction.guild.get_channel(staff_leave_channel_id)
        embed = discord.Embed(title=f"{interaction.user}'s Leave Request",
            description=f"""
**IGN**: {self.name.value}

**Date Leaving**: {self.dateleaving.value}

**Date Returning**: {self.datereturning.value}

**Reason**: {self.reason.value}
""",
        color=discord.Color.from_str(embed_color))
        await staff_leave_channel.send(embed=embed)
        await interaction.response.send_message("Submitted! \n \nA manager will approve your leave as soon as possible.", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        print(error)