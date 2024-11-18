import asyncio

import discord
from discord.ext import commands

from config import config

forum_tasks_id = config["Каналы"]["forum_tasks_id"]

class EventsModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.category_id == forum_tasks_id and message.content.startswith("(("):
            await asyncio.sleep(20)
            await message.delete()

def setup(bot):
    bot.add_cog(EventsModeration(bot))