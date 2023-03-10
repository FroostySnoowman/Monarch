import discord
import asyncio
import pytz
import yaml
from discord.ext import commands
from datetime import datetime

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
transcripts_channel_id = data["Tickets"]["TRANSCRIPTS_CHANNEL_ID"]

class TicketClose(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(emoji='🔒', label='Close', style=discord.ButtonStyle.gray, custom_id='ticketclose')
    async def ticketclose(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer(thinking=True, ephemeral=True)
    
            for item in self.children:
                item.disabled = True
            await interaction.message.edit(view=self)

            time = datetime.now(tz=pytz.timezone('America/Tijuana'))
            with open("transcripts.html", "w", encoding="utf-8") as file:
                msg = [message async for message in interaction.channel.history(oldest_first=True, limit=1)]
                firstmessagetime = msg[0].created_at.strftime("%m/%d/%y, %I:%M %p")
                y = msg[0].mentions[0]
                file.write(f"""<information> \nTicket Creator: {y} \nCreated At: {firstmessagetime} \nTicket Name: {interaction.channel} \n</information>
<!DOCTYPE html><html><head><title>Ticket Transcript</title><meta name='viewport' content='width=device-width, initial-scale=1.0'><meta charset='UTF-8'><link href='https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap' rel='stylesheet'></head><body><style>information {{display: none;}} body {{background-color: #181d23;color: white;font-family: 'Open-Sans', sans-serif;margin: 50px;}}.ticket-header h2 {{font-weight: 400;text-transform: capitalize;margin-bottom: 0;color: #fff;}}.ticket-header p {{font-size: 14px;}}.ticket-header .children .item {{margin-right: 25px;display: flex;align-items: center;}}.ticket-header .children {{display: flex;}}.ticket-header .children .item a {{margin-right: 7px;padding: 5px 10px;padding-top: 6px;background-color: #3c434b;border-radius: 3px;font-size: 12px;}}.messages {{margin-top: 30px;display: flex;flex-direction: column;}}.messages .item {{display: flex;margin-bottom: 20px;}}.messages .item .left img {{border-radius: 100%;height: 50px;}}.messages .item .left {{margin-right: 20px;}}.messages .item .right a:nth-child(1) {{font-weight: 400;margin: 0 15px 0 0;font-size: 19px;color: #fff;}}.messages .item .right a:nth-child(2) {{text-transform: capitalize;color: #ffffff;font-size: 12px;}}.messages .item .right div {{display: flex;align-items: center;margin-top: 5px;}}.messages .item .right p {{margin: 0;white-space: normal;line-height: 2;color: #fff;font-size: 15px;}}.messages .item .right p {{max-width: 700px;margin-top: 10px;}}.messages .item {{margin-bottom: 31px;}}@media  only screen and (max-width: 600px) {{body {{margin: 0px;padding: 25px;width: calc(100% - 50px);}}.ticket-header h2 {{margin-top: 0px;}}.ticket-header .children {{display: flex;flex-wrap: wrap;}}</style><div class='ticket-header'><h2>{interaction.channel} Transcript</h2><div class='children'><div class='item'><a>CREATED</a><p>{firstmessagetime} GMT</p></div><div class='item'><a>USER</a><p>{y}</p></div></div></div><div class='messages'><div class='item'><div class='left'><img src='{interaction.guild.icon}'> </div><div class='right'><div><a>{interaction.guild.name}</a><a></a></div><p>Transcript File For {interaction.guild.name}</p></div></div>
""")
                async for message in interaction.channel.history(limit=None, oldest_first=True):
                    msgtime = message.created_at.strftime("%m/%d/%y, %I:%M %p")
                    file.write(f"""<div class='item'><div class='left'><img src='{message.author.display_avatar.url}'> </div><div class='right'><div><a>{message.author}</a><a>{msgtime} GMT</a></div><p>{message.content}</p></div></div>""")
                file.write(f"""
<div class='item'><div class='left'><p>If a message is from a bot, and appears empty, its because the bot sent a message with no text, only an embed.</p></div></div>
</div></body></html>
""")
            with open("transcripts.html", "rb") as file:
                transcripts = interaction.guild.get_channel(transcripts_channel_id)
                msg = await discord.utils.get(interaction.channel.history(oldest_first=True, limit=1))
                time = pytz.timezone('America/Tijuana')
                created_at = msg.created_at
                now = datetime.now(time)
                maths = now - created_at
                seconds = maths.total_seconds()
                math = round(seconds)

                embed = discord.Embed(
                    title=f"Ticket Closed!",
                    description=
                    f"├ **Channel Name:** {interaction.channel.name} \n├ **Opened By:** {y.mention} \n├ **Opened ID:** {y.id} \n├ **Closed By:** {interaction.user.mention} \n├ **Closed ID:** {interaction.user.id} \n└ **Time Opened:** {math} Seconds",
                color=0x202225)
                await transcripts.send(embed=embed)
                await transcripts.send(file=discord.File(file, f"{interaction.channel.name}.html"))
            try:
                embed = discord.Embed(
                    title=f"Ticket Closed!",
                    description=
                    f"├ **Channel Name:** {interaction.channel.name} \n└ **Time Opened:** {math} Seconds",
                color=0x202225)
                embed.set_footer(text="You can view the transcript below.")
                await y.send(embed=embed)
                with open("transcripts.html", "rb") as file:
                    await y.send(file=discord.File(file, f"{interaction.channel.name}.html"))
            except:
                pass

            await interaction.followup.send('Ticket will close in 15 seconds.')
            await asyncio.sleep(15)
            await interaction.channel.delete()

class TicketCloseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(TicketClose())

async def setup(bot):
    await bot.add_cog(TicketCloseCog(bot), guilds=[discord.Object(id=guild_id)])