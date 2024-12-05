import asyncio

import discord
from discord import DMChannel
from discord.ext import commands

from config import config

forum_tasks_id = config.categories.forum_tasks_id
countdown = config.parameters.offtop_deletion_countdown

class EventsModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            print("\n\nnew message!")
            print(forum_tasks_id)
            print(message.channel.category_id)
            if message.channel.category_id == forum_tasks_id:
                print("it is in the forum tasks channel!")
                print("parsing channel history:")
                async for message_in_channel_history in message.channel.history(oldest_first = True):
                    print(f"   { message_in_channel_history}")
                    if message_in_channel_history.content.startswith("((") and message_in_channel_history.author == message.author and message_in_channel_history != message:
                        print("it is offtop")
                        print("removing...")
                        await asyncio.sleep(countdown)
                        await message_in_channel_history.delete()
                        break
        except AttributeError:
            pass
        except TypeError:
            pass

def setup(bot):
    bot.add_cog(EventsModeration(bot))
