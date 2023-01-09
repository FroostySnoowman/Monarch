import discord
import yaml
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
staff_guild_id = data["General"]["STAFF_GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
welcome_channel_id = data["Welcome"]["WELCOME_CHANNEL_ID"]
staff_welcome_channel_id = data["Welcome"]["STAFF_WELCOME_CHANNEL_ID"]

class JoinEventCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_member_join')
    async def on_member_join(self, member: discord.Member):
        guild = self.bot.get_guild(guild_id)
        staffguild = self.bot.get_guild(staff_guild_id)
        if member.guild == guild:
            channel = self.bot.get_channel(welcome_channel_id)
            embed = discord.Embed(title=f"Welcome, {member}!",
                description=f"Welcome to Monarch Network, {member.mention}!",
            color=discord.Color.from_str(embed_color))
            embed.add_field(name="Server IP", value="mc.monarchnetwork.xyz")
            embed.add_field(name="Website", value="https://monarchnetwork.xyz/")
            embed.add_field(name="Store", value="https://monarchnetwork.xyz/")
            embed.set_footer(text=member.guild.name, icon_url=member.guild.icon.url)
            await channel.send(embed=embed)
        if member.guild == staffguild:
            channel = self.bot.get_channel(staff_welcome_channel_id)
            embed = discord.Embed(title=f"Welcome, {member}!",
                description=f"""
Welcome to the Monarch Staff Discord Server, {member.mention}!
A manager will be with you shortly to verify you and start your training.
""",
            color=discord.Color.from_str(embed_color))
            embed.set_footer(text=member.guild.name, icon_url=member.guild.icon.url)
            await channel.send(embed=embed)
        else:
            return

async def setup(bot):
    await bot.add_cog(JoinEventCog(bot))