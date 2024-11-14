import discord
from discord.ext import commands

from config import channel_log_delete_id
from database import connection_mentions as connection, cursor_mentions as cursor
from classes import emojis

class EventsMentions(commands.Cog):
    def __init__(self, bot, channel_log_delete_id):
        self.bot = bot
        self.channel_log_delete_id = self.bot.get_channel(channel_log_delete_id)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        mention_names = [mention_name[0] for mention_name in cursor.execute(f"SELECT name FROM mentions").fetchall()]
        for mention_name in mention_names:
            mention_members = cursor.execute(f"SELECT members FROM mentions WHERE name = '{mention_name}'").fetchone()[0].split(".")
            if str(member.id) in mention_members:
                mention_members.remove(str(member.id))
                if len(mention_members) == 1:
                    cursor.execute(f"DELETE FROM mentions WHERE name = '{mention_name}'")
                    connection.commit()
                    await self.channel_log_delete.send(f"{emojis.delete} Рассылка \"`{mention_name}`\" была удалена автоматически.")
                else:
                    cursor.execute(f"UPDATE mentions SET members = '{'.'.join(mention_members)}' WHERE name = '{mention_name}'")
                    connection.commit()

def setup(bot):
    bot.add_cog(EventsMentions(bot, channel_log_delete_id))