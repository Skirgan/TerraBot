import asyncio

import discord
from discord import DMChannel
from discord.ext import commands

from config import config, read_config
import config as config_file

forum_tasks_id = config.categories.forum_tasks_id
countdown = config.parameters.offtop_deletion_countdown

class EventsModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            print(f"\n\nnew message: {message.content}")
            print(forum_tasks_id)
            print(message.channel.category_id)
            if message.channel.category_id == forum_tasks_id:
                print("it is in the forum tasks channel!")
                print("parsing channel history:")
                async for message_in_channel_history in message.channel.history(oldest_first = True):
                    print(f"  \"{message_in_channel_history.content}\"")
                    if message_in_channel_history.content.startswith("((") and message_in_channel_history.author == message.author and message_in_channel_history != message:
                        print("this is offtop")
                        print(f"removing in {countdown} seconds...")
                        await asyncio.sleep(countdown)
                        print("removed")
                        await message_in_channel_history.delete()
                        break
        except AttributeError:
            pass
        except TypeError:
            pass

def setup(bot):
    bot.add_cog(EventsModeration(bot))
