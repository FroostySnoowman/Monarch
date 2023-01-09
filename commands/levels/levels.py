import discord
import aiosqlite
import yaml
from discord import app_commands
from discord.ext import commands
from typing import Optional

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
level_xp = data["Levels"]["LEVEL_XP"]

class LevelCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="level", description="Shows you your level!")
    @app_commands.describe(member="Who's level would you like to view?")
    async def level(self, interaction: discord.Interaction, member: Optional[discord.Member]) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        db = await aiosqlite.connect('database.db')
        if member is None:
            cursor = await db.execute('SELECT * from levels WHERE user_id=?', (interaction.user.id, ))
            a = await cursor.fetchone()
            if a is None:
                embed = discord.Embed(description="You have no information to show!", color=discord.Color.red())
                await interaction.followup.send(embed=embed)
            else:
                xp_needed = level_xp.get(f'{a[2]}')
                embed = discord.Embed(color=discord.Color.from_str(embed_color))
                embed.add_field(name="Level", value=f"**{a[2]}**")
                embed.add_field(name="Experience", value=f"**{a[1]}**/**{xp_needed}**")
                embed.add_field(name="Message Experience", value=f"<t:{a[3]}:R>")
                cursor2 = await db.execute('SELECT * from voice WHERE user_id=?', (interaction.user.id, ))
                b = await cursor2.fetchone()
                if b is None:
                    pass
                else:
                    embed.add_field(name="Voice Experience", value=f"<t:{b[1]}:R>")
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                cursor3 = await db.execute('SELECT * from levels ORDER BY level DESC')
                c = await cursor3.fetchall()
                outof = 0
                for d in c:
                    outof += 1
                for i, val in enumerate(c):
                    if val[0] == interaction.user.id:
                        i += 1
                        embed.add_field(name="Rank", value=f"**#{i}**/**{outof}**")
                await interaction.followup.send(embed=embed)
        else:
            cursor = await db.execute('SELECT * from levels WHERE user_id=?', (member.id, ))
            a = await cursor.fetchone()
            if a is None:
                embed = discord.Embed(description=f"{member.mention} has no information to show!", color=discord.Color.red())
                await interaction.followup.send(embed=embed)
            else:
                xp_needed = level_xp.get(f'{a[2]}')
                embed = discord.Embed(color=discord.Color.from_str(embed_color))
                embed.add_field(name="Level", value=f"**{a[2]}**")
                embed.add_field(name="Experience", value=f"**{a[1]}**/**{xp_needed}**")
                embed.set_author(name=member.name, icon_url=member.display_avatar.url)
                cursor2 = await db.execute('SELECT * from levels ORDER BY level DESC')
                b = await cursor2.fetchall()
                outof = 0
                for d in b:
                    outof += 1
                for i, val in enumerate(b):
                    if val[0] == member.id:
                        i += 1
                        embed.add_field(name="Rank", value=f"**#{i}**/**{outof}**")
                await interaction.followup.send(embed=embed)
        await db.close()

    @app_commands.command(name="rank", description="Shows you your rank!")
    @app_commands.describe(member="Who's rank would you like to view?") 
    async def rank(self, interaction: discord.Interaction, member: Optional[discord.Member]) -> None:
        db = await aiosqlite.connect('database.db')
        if member is None:
            cursor = await db.execute('SELECT * from levels ORDER BY level DESC')
            a = await cursor.fetchall()
            if a is None:
                embed = discord.Embed(description="You have no information to show!", color=discord.Color.red())
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                outof = 0
                for i in a:
                    outof += 1
                for i, val in enumerate(a):
                    if val[0] == interaction.user.id:
                        embed = discord.Embed(color=discord.Color.from_str(embed_color))
                        i += 1
                        embed.add_field(name="Rank", value=f"**#{i}**/**{outof}**")
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            cursor = await db.execute('SELECT * from levels ORDER BY level DESC')
            a = await cursor.fetchall()
            if a is None:
                embed = discord.Embed(description=f"{member.mention} has no information to show!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                outof = 0
                for i in a:
                    outof += 1
                for i, val in enumerate(a):
                    if val[0] == member.id:
                        embed = discord.Embed(color=discord.Color.from_str(embed_color))
                        i += 1
                        embed.add_field(name="Rank", value=f"**#{i}**/**{outof}**")
                embed.set_author(name=member.name, icon_url=member.display_avatar.url)
                await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.close()

    @app_commands.command(name="leaderboard", description="Shows the level leaderboard!")
    async def leaderboard(self, interaction: discord.Interaction) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from levels ORDER BY level DESC')
        a = await cursor.fetchall()
        if a is None:
            embed = discord.Embed(description="There is no information to show!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            var = ""
            num = 0
            for i in a:
                num += 1
            for i, val in enumerate(a):
                var = var+f" \n**#{num}** Level **{val[2]}** <@{val[0]}>"
            embed = discord.Embed(title=f"{interaction.guild.name} Leaderboard", description=var, color=discord.Color.from_str(embed_color))
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(LevelCog(bot), guilds=[discord.Object(id=guild_id)])