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
                async for message_in_channel_history in message.channel.history(limit = None, oldest_first = True):
                    if (message_in_channel_history.content.startswith("((") or message_in_channel_history.content.startswith("//"))and message_in_channel_history.author == message.author and message_in_channel_history != message:
                        await asyncio.sleep(7)
                        try:
                            await message_in_channel_history.delete()
                        except:
                            pass
                        break
        except AttributeError:
            pass

def setup(bot):
    bot.add_cog(EventsModeration(bot))