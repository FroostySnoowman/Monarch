import discord
import datetime as DT
import aiosqlite
import random
import yaml
from discord.ext import commands
from datetime import datetime, timedelta

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
staff_guild_id = data["General"]["STAFF_GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
level_xp = data["Levels"]["LEVEL_XP"]
max_random_xp = data["Levels"]["MAX_RANDOM_XP"]
active_role_id= data["Levels"]["ACTIVE_ROLE_ID"]
level_10_role_id = data["Levels"]["LEVEL_10_ROLE_ID"]
level_20_role_id = data["Levels"]["LEVEL_20_ROLE_ID"]
level_35_role_id = data["Levels"]["LEVEL_35_ROLE_ID"]
level_50_role_id = data["Levels"]["LEVEL_50_ROLE_ID"]

class MessageEventCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_message')
    async def on_message(self, message: discord.Message):
        guild = self.bot.get_guild(guild_id)
        staffguild = self.bot.get_guild(staff_guild_id)
        if message.guild == guild:
            if message.author.bot:
                return
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * from levels WHERE user_id=?', (message.author.id, ))
            a = await cursor.fetchone()
            random_xp = random.randint(1,max_random_xp)
            x = datetime.now() + timedelta(seconds=60)
            cooldown_timestamp = int(x.timestamp())
            if a is None:
                await db.execute('INSERT INTO levels VALUES (?,?,?,?);', (message.author.id, random_xp, 1, cooldown_timestamp))
            else:
                xp = a[1] + random_xp
                level = a[2]
                stored_cooldown_timestamp = a[3]
                if level == 100:
                    await db.close()
                    return
                if stored_cooldown_timestamp <= DT.datetime.now().timestamp():
                    xp_needed = level_xp.get(f'{level}')
                    if xp >= xp_needed:
                        await db.execute('UPDATE levels SET level=level+? WHERE user_id=?', (1, message.author.id))
                        if level+1 == 5:
                            active_role = message.guild.get_role(active_role_id)
                            await message.author.add_roles(active_role)
                        if level+1 == 10:
                            level_10_role = message.guild.get_role(level_10_role_id)
                            await message.author.add_roles(level_10_role)
                        if level+1 ==20:
                            level_20_role = message.guild.get_role(level_20_role_id)
                            await message.author.add_roles(level_20_role)
                        if level+1 == 35:
                            level_35_role = message.guild.get_role(level_35_role_id)
                            await message.author.add_roles(level_35_role)
                        if level+1 == 50:
                            level_50_role = message.guild.get_role(level_50_role_id)
                            await message.author.add_roles(level_50_role)
                        embed = discord.Embed(description=f"GG, {message.author.mention}, you just advanced to level **{level+1}**!", color=discord.Color.from_str(embed_color))
                        embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
                        await message.reply(embed=embed)
                    await db.execute('UPDATE levels SET cooldown=? WHERE user_id=?', (cooldown_timestamp, message.author.id))
                    await db.execute('UPDATE levels SET experience=? WHERE user_id=?', (xp, message.author.id))
            await db.commit()
            await db.close()
        if message.guild == staffguild:
            return
        else:
            return

async def setup(bot):
    await bot.add_cog(MessageEventCog(bot))