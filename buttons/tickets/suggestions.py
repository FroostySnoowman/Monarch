import discord
import aiosqlite
import yaml
from discord.ext import commands

from modals.tickets.staffleave import StaffLeave

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
accepted_embed_color = data["Suggestions"]["ACCEPTED_EMBED_COLOR"]
denied_embed_color = data["Suggestions"]["DENIED_EMBED_COLOR"]
suggestions_channel_id = data["Suggestions"]["SUGGESTIONS_CHANNEL_ID"]
responses_channel_id = data["Suggestions"]["RESPONSES_CHANNEL_ID"]
staff_suggestions_channel_id = data["Suggestions"]["STAFF_SUGGESTIONS_CHANNEL_ID"]
staff_responses_channel_id = data["Suggestions"]["STAFF_RESPONSES_CHANNEL_ID"]

class VotingSystem(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='👍', style=discord.ButtonStyle.grey, custom_id='voting:1', row=1)
    async def upvote(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM suggestions WHERE message_id=?', (interaction.message.id, ))
        a = await cursor.fetchone()
        if a[6] == 'null':
            stored = f"{interaction.user.id}"
        else:
            user_id = f"{interaction.user.id}"
            stringded = str(a[6])
            if user_id in stringded:
                await interaction.response.send_message("You've already voted!", ephemeral=True)
                await db.close()
                return
            else:
                d = str(a[6])
                stored = ", ".join([d, "".join(user_id)])
        upvotes = a[7] + 1
        downvotes = a[8]
        await db.execute('UPDATE suggestions SET upvotes=? WHERE message_id=?', (upvotes, interaction.message.id))
        await db.execute('UPDATE suggestions SET voters=? WHERE message_id=?', (stored, interaction.message.id))
        member = interaction.guild.get_member(a[0])
        embed = discord.Embed(title=f"{member}'s Suggestion",
            description=f"""
**Server**: {a[1]}

**Suggestion**: {a[2]}

**Reason**: {a[3]}

**Status**: __Pending__

Upvotes: {upvotes}
Downvotes: {downvotes}
""",
        color=discord.Color.from_str(embed_color))
        await interaction.response.edit_message(embed=embed)
        await db.commit()
        await db.close()

    @discord.ui.button(emoji='👎', style=discord.ButtonStyle.grey, custom_id='voting:2', row=1)
    async def downvote(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM suggestions WHERE message_id=?', (interaction.message.id, ))
        a = await cursor.fetchone()
        if a[6] == 'null':
            stored = f"{interaction.user.id}"
        else:
            user_id = f"{interaction.user.id}"
            stringded = str(a[6])
            if user_id in stringded:
                await interaction.response.send_message("You've already voted!", ephemeral=True)
                await db.close()
                return
            else:
                d = str(a[6])
                stored = ", ".join([d, "".join(user_id)])
        upvotes = a[7]
        downvotes = a[8] + 1
        await db.execute('UPDATE suggestions SET downvotes=? WHERE message_id=?', (downvotes, interaction.message.id))
        await db.execute('UPDATE suggestions SET voters=? WHERE message_id=?', (stored, interaction.message.id))
        member = interaction.guild.get_member(a[0])
        embed = discord.Embed(title=f"{member}'s Suggestion",
            description=f"""
**Server**: {a[1]}

**Suggestion**: {a[2]}

**Reason**: {a[3]}

**Status**: __Pending__

Upvotes: {upvotes}
Downvotes: {downvotes}
""",
        color=discord.Color.from_str(embed_color))
        await interaction.response.edit_message(embed=embed)
        await db.commit()
        await db.close()

class SuggestionsSystem(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='✅', label='Approve', style=discord.ButtonStyle.grey, custom_id='suggestions:1')
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.guild_permissions.administrator:
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * FROM suggestions WHERE response_message_id=?', (interaction.message.id, ))
            a = await cursor.fetchone()
            suggestion_channel = interaction.guild.get_channel(suggestions_channel_id)
            suggestion_message = suggestion_channel.get_partial_message(a[4])
            await suggestion_message.delete()
            member = interaction.guild.get_member(a[0])
            embed = discord.Embed(title=f"{member}'s Suggestion",
                description=f"""
**Server**: {a[1]}

**Suggestion**: {a[2]}

**Reason**: {a[3]}

**Status**: __Accepted__

Upvotes: {a[7]}
Downvotes: {a[8]}
""",
            color=discord.Color.from_str(accepted_embed_color))
            await interaction.response.edit_message(embed=embed, view=None)
            await db.execute('DELETE FROM suggestions WHERE response_message_id=?', (interaction.message.id, ))
            await db.commit()
            await db.close()
        else:
            await interaction.response.send_message("You don't have the correct permissions to use this button!", ephemeral=True)

    @discord.ui.button(emoji='❌', label='Deny', style=discord.ButtonStyle.grey, custom_id='suggestions:2')
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.guild_permissions.administrator:
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * FROM suggestions WHERE response_message_id=?', (interaction.message.id, ))
            a = await cursor.fetchone()
            suggestion_channel = interaction.guild.get_channel(suggestions_channel_id)
            suggestion_message = suggestion_channel.get_partial_message(a[4])
            await suggestion_message.delete()
            member = interaction.guild.get_member(a[0])
            embed = discord.Embed(title=f"{member}'s Suggestion",
                description=f"""
**Server**: {a[1]}

**Suggestion**: {a[2]}

**Reason**: {a[3]}

**Status**: __Denied__

Upvotes: {a[7]}
Downvotes: {a[8]}
""",
            color=discord.Color.from_str(denied_embed_color))
            await interaction.response.edit_message(embed=embed, view=None)
            await db.execute('DELETE FROM suggestions WHERE response_message_id=?', (interaction.message.id, ))
            await db.commit()
            await db.close()
        else:
            await interaction.response.send_message("You don't have the correct permissions to use this button!", ephemeral=True)


class StaffSuggestions(discord.ui.Modal, title='Suggestions'):

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
        suggestions = interaction.guild.get_channel(staff_suggestions_channel_id)
        responses = interaction.guild.get_channel(staff_responses_channel_id)
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
        a = await suggestions.send(embed=embed, view=StaffVotingSystem())
        b = await responses.send(embed=embed2, view=StaffSuggestionsSystem())
        await db.execute('INSERT INTO suggestions VALUES (?,?,?,?,?,?,?,?,?);', (interaction.user.id, self.server.value, self.suggestion.value, self.reason.value, a.id, b.id, "null", 0, 0))
        await db.commit()
        await db.close()
        await interaction.response.send_message('Submitted!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        print(error)

class StaffTickets(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='📆', label='Staff Leave', style=discord.ButtonStyle.grey, custom_id='stafftickets:1')
    async def staffleave(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(StaffLeave())

    @discord.ui.button(emoji='🗣️', label='Suggestions', style=discord.ButtonStyle.grey, custom_id='stafftickets:2')
    async def staffsuggestions(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(StaffSuggestions())

class StaffVotingSystem(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='👍', style=discord.ButtonStyle.grey, custom_id='staffvoting:1', row=1)
    async def staffpvote(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM suggestions WHERE message_id=?', (interaction.message.id, ))
        a = await cursor.fetchone()
        if a[6] == 'null':
            stored = f"{interaction.user.id}"
        else:
            user_id = f"{interaction.user.id}"
            stringded = str(a[6])
            if user_id in stringded:
                await interaction.response.send_message("You've already voted!", ephemeral=True)
                await db.close()
                return
            else:
                d = str(a[6])
                stored = ", ".join([d, "".join(user_id)])
        upvotes = a[7] + 1
        downvotes = a[8]
        await db.execute('UPDATE suggestions SET upvotes=? WHERE message_id=?', (upvotes, interaction.message.id))
        await db.execute('UPDATE suggestions SET voters=? WHERE message_id=?', (stored, interaction.message.id))
        member = interaction.guild.get_member(a[0])
        embed = discord.Embed(title=f"{member}'s Suggestion",
            description=f"""
**Server**: {a[1]}

**Suggestion**: {a[2]}

**Reason**: {a[3]}

**Status**: __Pending__

Upvotes: {upvotes}
Downvotes: {downvotes}
""",
        color=discord.Color.from_str(embed_color))
        await interaction.response.edit_message(embed=embed)
        await db.commit()
        await db.close()

    @discord.ui.button(emoji='👎', style=discord.ButtonStyle.grey, custom_id='staffvoting:2', row=1)
    async def staffdownvote(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM suggestions WHERE message_id=?', (interaction.message.id, ))
        a = await cursor.fetchone()
        if a[6] == 'null':
            stored = f"{interaction.user.id}"
        else:
            user_id = f"{interaction.user.id}"
            stringded = str(a[6])
            if user_id in stringded:
                await interaction.response.send_message("You've already voted!", ephemeral=True)
                await db.close()
                return
            else:
                d = str(a[6])
                stored = ", ".join([d, "".join(user_id)])
        upvotes = a[7]
        downvotes = a[8] + 1
        await db.execute('UPDATE suggestions SET downvotes=? WHERE message_id=?', (downvotes, interaction.message.id))
        await db.execute('UPDATE suggestions SET voters=? WHERE message_id=?', (stored, interaction.message.id))
        member = interaction.guild.get_member(a[0])
        embed = discord.Embed(title=f"{member}'s Suggestion",
            description=f"""
**Server**: {a[1]}

**Suggestion**: {a[2]}

**Reason**: {a[3]}

**Status**: __Pending__

Upvotes: {upvotes}
Downvotes: {downvotes}
""",
        color=discord.Color.from_str(embed_color))
        await interaction.response.edit_message(embed=embed)
        await db.commit()
        await db.close()

class StaffSuggestionsSystem(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='✅', label='Approve', style=discord.ButtonStyle.grey, custom_id='staffsuggestions:1')
    async def staffapprove(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.guild_permissions.administrator:
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * FROM suggestions WHERE response_message_id=?', (interaction.message.id, ))
            a = await cursor.fetchone()
            suggestion_channel = interaction.guild.get_channel(staff_suggestions_channel_id)
            suggestion_message = suggestion_channel.get_partial_message(a[4])
            await suggestion_message.delete()
            member = interaction.guild.get_member(a[0])
            embed = discord.Embed(title=f"{member}'s Suggestion",
                description=f"""
**Server**: {a[1]}

**Suggestion**: {a[2]}

**Reason**: {a[3]}

**Status**: __Accepted__

Upvotes: {a[7]}
Downvotes: {a[8]}
""",
            color=discord.Color.from_str(accepted_embed_color))
            await interaction.response.edit_message(embed=embed, view=None)
            await db.execute('DELETE FROM suggestions WHERE response_message_id=?', (interaction.message.id, ))
            await db.commit()
            await db.close()
        else:
            await interaction.response.send_message("You don't have the correct permissions to use this button!", ephemeral=True)

    @discord.ui.button(emoji='❌', label='Deny', style=discord.ButtonStyle.grey, custom_id='staffsuggestions:2')
    async def staffdeny(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.guild_permissions.administrator:
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * FROM suggestions WHERE response_message_id=?', (interaction.message.id, ))
            a = await cursor.fetchone()
            suggestion_channel = interaction.guild.get_channel(staff_suggestions_channel_id)
            suggestion_message = suggestion_channel.get_partial_message(a[4])
            await suggestion_message.delete()
            member = interaction.guild.get_member(a[0])
            embed = discord.Embed(title=f"{member}'s Suggestion",
                description=f"""
**Server**: {a[1]}

**Suggestion**: {a[2]}

**Reason**: {a[3]}

**Status**: __Denied__

Upvotes: {a[7]}
Downvotes: {a[8]}
""",
            color=discord.Color.from_str(denied_embed_color))
            await interaction.response.edit_message(embed=embed, view=None)
            await db.execute('DELETE FROM suggestions WHERE response_message_id=?', (interaction.message.id, ))
            await db.commit()
            await db.close()
        else:
            await interaction.response.send_message("You don't have the correct permissions to use this button!", ephemeral=True)

class SuggestionsSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(VotingSystem())
        self.bot.add_view(SuggestionsSystem())
        self.bot.add_view(StaffVotingSystem())
        self.bot.add_view(SuggestionsSystem())
        self.bot.add_view(StaffTickets())

async def setup(bot):
    await bot.add_cog(SuggestionsSystemCog(bot), guilds=[discord.Object(id=guild_id)])