import datetime
import discord
from pycord.multicog import Bot
import os
from colorama import init, Fore, Style
from extensions import *
from config import token

intents = discord.Intents.default()
intents = discord.Intents.all()
bot = Bot(intents = intents)
bot.auto_sync_commands = False

@bot.event
async def on_ready():
    black_list_files = ["__init__.py", "functions.py"]
    for directory, directories, files in os.walk("./extensions"):
        for file in os.listdir(directory):
            if file.endswith(".py") and file not in black_list_files:
                print(f"{Fore.BLUE}·{Fore.RESET} {Fore.CYAN}Попытка загрузки{Fore.RESET}: {directory[2:]}.{file}", end = "")
                try:
                    str_for_load = f"{directory[2:]}.{file[:-3]}".replace("\\", ".")
                    bot.load_extension(str_for_load)
                    print(f" —— {Fore.GREEN}успешно{Fore.RESET}")
                except:
                    print(f" —— {Fore.RED}безуспешно{Fore.RESET}")
    if not bot.auto_sync_commands:
        await bot.sync_commands(guild_ids = [787280396915048498])

    print(f"\nПодключённые команды:")
    for cog in list(bot.cogs.keys()):
        for command in bot.get_cog(cog).get_commands():
            if type(command) == discord.SlashCommand:
                print(f"{Fore.BLUE}·{Fore.RESET} {Fore.CYAN}{command}{Fore.RESET} (команда)")
            elif type(command) == discord.SlashCommandGroup:
                print(f"{Fore.BLUE}·{Fore.RESET} {Fore.CYAN}{command}{Fore.RESET} (группа):")
                for command_in_group in command.walk_commands():
                    print(f"    {Fore.BLUE}·{Fore.RESET} {Fore.CYAN}{command_in_group}{Fore.RESET} (команда)")
            else:
                print(type(command))
        for event in bot.get_cog(cog).get_listeners():
            print(f"{Style.DIM}{Fore.YELLOW}·{Fore.RESET}{Style.RESET_ALL} {Fore.YELLOW}{event[0]}{Fore.RESET} (обработчик)")

    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.custom, state = f"Запуск произведён {datetime.datetime.now().strftime('%H:%M:%S')}"))

bot.run(token)