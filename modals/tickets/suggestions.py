import discord
import aiosqlite
import yaml

from buttons.tickets.suggestions import SuggestionsSystem
from buttons.tickets.suggestions import VotingSystem

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = data["General"]["EMBED_COLOR"]
suggestions_channel_id = data["Suggestions"]["SUGGESTIONS_CHANNEL_ID"]
responses_channel_id = data["Suggestions"]["RESPONSES_CHANNEL_ID"]

class Suggestions(discord.ui.Modal, title='Suggestions'):

    server = discord.ui.TextInput(
        label="What server is this suggestion for?",
        placeholder="Type the server here...",
        max_length=50,
        style=discord.TextStyle.paragraph,
    )

    suggestion = discord.ui.TextInput(
        label="What is your suggestion?",
        placeholder="Type your suggestion here...",
        max_length=1500,
        style=discord.TextStyle.paragraph,
    )

    reason = discord.ui.TextInput(
        label='What is the reason for the suggestion?',
        placeholder='Type the reason here...',
        max_length=1500,
        style=discord.TextStyle.paragraph,
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        suggestions = interaction.guild.get_channel(suggestions_channel_id)
        responses = interaction.guild.get_channel(responses_channel_id)
        embed = discord.Embed(title=f"{interaction.user}'s Suggestion",
            description=f"""
**Server**: {self.server.value}

**Suggestion**: {self.suggestion.value}

**Reason**: {self.reason.value}

**Status**: __Pending__

Upvotes: 0
Downvotes: 0
""",
        color=discord.Color.from_str(embed_color))
        embed2 = discord.Embed(title=f"{interaction.user}'s Suggestion",
            description=f"""
**Server**: {self.server.value}

**Suggestion**: {self.suggestion.value}

**Reason**: {self.reason.value}

**Status**: __Pending__

""",
        color=discord.Color.from_str(embed_color))
        a = await suggestions.send(embed=embed, view=VotingSystem())
        b = await responses.send(embed=embed2, view=SuggestionsSystem())
        await db.execute('INSERT INTO suggestions VALUES (?,?,?,?,?,?,?,?,?);', (interaction.user.id, self.server.value, self.suggestion.value, self.reason.value, a.id, b.id, "null", 0, 0))
        await db.commit()
        await db.close()
        await interaction.response.send_message('Submitted!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        print(error)