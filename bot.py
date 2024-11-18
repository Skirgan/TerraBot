import discord
from pycord.multicog import Bot

intents = discord.Intents.default()
# intents = discord.Intents.all()
bot = Bot(intents = intents)
