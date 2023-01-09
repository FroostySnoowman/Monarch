import discord
import aiosqlite
import datetime as DT
import random
import yaml
from discord.ext import commands, tasks
from datetime import datetime, timedelta

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
staff_guild_id = data["General"]["STAFF_GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
afk_channel_id = data["Levels"]["AFK_CHANNEL_ID"]
level_xp = data["Levels"]["LEVEL_XP"]
max_random_xp = data["Levels"]["MAX_RANDOM_XP"]
active_role_id= data["Levels"]["ACTIVE_ROLE_ID"]
level_10_role_id = data["Levels"]["LEVEL_10_ROLE_ID"]
level_20_role_id = data["Levels"]["LEVEL_20_ROLE_ID"]
level_35_role_id = data["Levels"]["LEVEL_35_ROLE_ID"]
level_50_role_id = data["Levels"]["LEVEL_50_ROLE_ID"]

class VoiceEventsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def cog_load(self):
        self.voiceLoop.start()

    @tasks.loop(seconds = 5)
    async def voiceLoop(self):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from voice')
        a = await cursor.fetchall()
        if a is None:
            pass
        else:
            for x in a:
                if x[1] <= DT.datetime.now().timestamp():
                    guild = self.bot.get_guild(guild_id)
                    member = guild.get_member(x[0])
                    cursor2 = await db.execute('SELECT * from levels WHERE user_id=?', (x[0], ))
                    b = await cursor2.fetchone()
                    ts = datetime.now() + timedelta(seconds=60)
                    cooldown_timestamp = int(ts.timestamp())
                    random_xp = random.randint(1,max_random_xp)
                    if str(member.voice.channel) == "AFK":
                        if b is None:
                            await db.execute('INSERT INTO levels VALUES (?,?,?,?);', (x[0], 0, 1, cooldown_timestamp))
                            await db.execute('UPDATE voice SET cooldown=? WHERE user_id=?', (cooldown_timestamp, x[0]))
                        else:
                            await db.execute('UPDATE levels SET experience=experience+? WHERE user_id=?', (0, x[0]))
                            await db.execute('UPDATE voice SET cooldown=? WHERE user_id=?', (cooldown_timestamp, x[0]))
                    else:
                        if b is None:
                            await db.execute('INSERT INTO levels VALUES (?,?,?,?);', (x[0], random_xp, 1, cooldown_timestamp))
                            await db.execute('UPDATE voice SET cooldown=? WHERE user_id=?', (cooldown_timestamp, x[0]))
                        else:
                            await db.execute('UPDATE levels SET experience=experience+? WHERE user_id=?', (random_xp, x[0]))
                            await db.execute('UPDATE voice SET cooldown=? WHERE user_id=?', (cooldown_timestamp, x[0]))
                else:
                    pass
        await db.commit()
        await db.close()

    @voiceLoop.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = self.bot.get_guild(guild_id)
        if member.guild == guild:
            db = await aiosqlite.connect('database.db')
            if after.channel and not before.channel:
                if after.channel.id == afk_channel_id:
                    pass
                else:
                    cursor = await db.execute('SELECT * from levels WHERE user_id=?', (member.id, ))
                    a = await cursor.fetchone()
                    cursor2 = await db.execute('SELECT * from voice WHERE user_id=?', (member.id, ))
                    b = await cursor2.fetchone()
                    random_xp = random.randint(1,max_random_xp)
                    x = datetime.now() + timedelta(seconds=60)
                    cooldown_timestamp = int(x.timestamp())
                    if a is None:
                        await db.execute('INSERT INTO levels VALUES (?,?,?,?);', (member.id, random_xp, 1, cooldown_timestamp))
                    else:
                        if b is None:
                            await db.execute('INSERT INTO voice VALUES (?,?);', (member.id, cooldown_timestamp))
                        else:
                            pass
            if before.channel and not after.channel:
                cursor = await db.execute('SELECT * from voice WHERE user_id=?', (member.id, ))
                a = await cursor.fetchone()
                if a is None:
                    pass
                else:
                    await db.execute('DELETE FROM voice WHERE user_id=?', (member.id, ))
            await db.commit()
            await db.close()
        else:
            return

async def setup(bot):
    await bot.add_cog(VoiceEventsCog(bot))