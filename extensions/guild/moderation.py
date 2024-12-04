import asyncio

import discord
from discord import DMChannel
from discord.ext import commands

from config import config

forum_tasks_id = config.channels.forum_tasks_id
countdown = config.parameters.offtop_deletiob_countdown

class EventsModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.channel.category_id == forum_tasks_id:
               async for message_in_channel_history in message.channel.history(oldest_first = True):
                   if message_in_channel_history.content.startswith("((") and message_in_channel_history.author == message.author and message_in_channel_history != message:
                       await asyncio.sleep(countdown)
                       await message_in_channel_history.delete()
                       break
        except AttributeError:
            pass
        except TypeError:
            pass

def setup(bot):
    bot.add_cog(EventsModeration(bot))
