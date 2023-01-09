import discord
import yaml
from discord import app_commands
from discord.ext import commands

from buttons.verification.verification import VerificationSystem

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]

class VerificationCog(commands.GroupCog, name="verification"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 

    @app_commands.command(name="panel", description="Sends the verification panel.")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.default_permissions(administrator=True)
    async def panel(self, interaction: discord.Interaction):
        view = VerificationSystem()
        embed = discord.Embed(title="MonarchNetwork Discord Guidelines",
            description="""
All rules listed are subject to change at any time. Please follow all rules and guidelines when interacting with the community.

All punishments are staff discretionary, any punishment questions/appeals can be made in the <#840645535206998086> channel.

**Rules**:

**Toxicity**:
Toxicity in any form will not be tolerated. This includes harassing, bullying, and demeaning other members. Everyone is to be treated respectfully.

**Scamming**:
Scamming of any kind is not allowed and will result in immediate removal from the server.

**Explicit Content**:
You may not post any explicit comments, images, or links. Anything that is not deemed appropriate will be deleted.

**Spam/Character Spam**:
Do not spam or flood the text channels, you will be muted.

**Derogatory Comments**:
You may not use any homophobic, racial, or derogatory slurs. Using slurs to insult, harm or abuse a member will result in punishment.

**Staff Disrespect/Harassment**:
Treat staff with respect. They are here to help and answer questions; any kind of disrespect towards them wont be tolerated.

**Abusing Voice Channels**:
You may not use voice changers/distorters when talking in the voice channels nor may you scream or blast music into the channels.

**Abusing Rules**:
Attempting to abuse or bend the rules in any way is not allowed. This will be at staff's discretion.

**Advertising**:
Advertising other servers or discords is not allowed and will result in a permanent removal from the server.
""",
            color=discord.Color.from_str(embed_color))
        embed.set_footer(text="Clicking the button below will grant you access to the rest of the server.")
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message('Sent!', ephemeral=True)

async def setup(bot):
    await bot.add_cog(VerificationCog(bot), guilds=[discord.Object(id=guild_id)])