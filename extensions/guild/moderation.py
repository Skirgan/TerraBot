import asyncio

import discord
from discord.ext import commands

from config import forum_tasks_id

class EventsModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.channel.category_id == forum_tasks_id:
               for message_in_channel_history in message.channel.history(oldest_first = True):
                   if message_in_channel_history.content.startswith("((") and message_in_channel_history.author == message.author:
                       await asyncio.sleep(10)
                       await message_in_channel_history.delete()
                       break
        except AttributeError:
            pass
        except TypeError:
            pass

def setup(bot):
    bot.add_cog(EventsModeration(bot))