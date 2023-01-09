import discord
import yaml
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
member_role_id = data["Verification"]["MEMBER_ROLE_ID"]
muted_role_id = data["Verification"]["MUTED_ROLE_ID"]

class VerificationSystem(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='✅', label='Verify', style=discord.ButtonStyle.grey, custom_id='verify:1')
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = discord.utils.get(interaction.guild.roles, id=member_role_id)
        muted = discord.utils.get(interaction.guild.roles, id=muted_role_id)
        if member in interaction.user.roles:
            await interaction.response.send_message("You can't unverify yourself!", ephemeral=True)
            return
        if muted in interaction.user.roles:
            await interaction.response.send_message("Don't try to get around a mute!", ephemeral=True)
            return
        else:
            await interaction.user.add_roles(member)
            await interaction.response.send_message('You have sucessfully been verified!', ephemeral=True)
            return

class VerificationSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(VerificationSystem())

async def setup(bot):
    await bot.add_cog(VerificationSystemCog(bot), guilds=[discord.Object(id=guild_id)])