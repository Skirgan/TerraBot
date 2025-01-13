from types import MethodType

import discord
from pycord.multicog import Bot
from colorama import Fore

intents = discord.Intents.default()
# intents = discord.Intents.all()
bot = Bot(intents = intents)

def load(self, extension) -> bool:
    print(f"{Fore.BLUE}·{Fore.RESET} {Fore.CYAN}Попытка загрузки{Fore.RESET}: {extension}.py", end = "")
    try:
        self.load_extension(extension)
    except Exception as err:
        print(f" —— {Fore.RED}безуспешно: {err}{Fore.RESET}")
        return False
    else:
        print(f" —— {Fore.GREEN}успешно{Fore.RESET}")
        return True

def print_commands(self):
    print(f"\nПодключённые команды:")
    for cog in list(self.cogs.keys()):
        for command in self.get_cog(cog).get_commands():
            if type(command) == discord.SlashCommand:
                print(f"{Fore.BLUE}·{Fore.RESET} {Fore.CYAN}{command}{Fore.RESET} (команда)")
            elif type(command) == discord.SlashCommandGroup:
                print(f"{Fore.BLUE}·{Fore.RESET} {Fore.CYAN}{command}{Fore.RESET} (группа):")
                for command_in_group in command.walk_commands():
                    print(f"    {Fore.BLUE}·{Fore.RESET} {Fore.CYAN}{command_in_group}{Fore.RESET} (команда)")
            else:
                print(type(command))
        for event in self.get_cog(cog).get_listeners():
            print(f"{Style.DIM}{Fore.YELLOW}·{Fore.RESET}{Style.RESET_ALL} {Fore.YELLOW}{event[0]}{Fore.RESET} (обработчик)")



bot.load = MethodType(load, bot)
bot.print_commands = MethodType(print_commands, bot)
