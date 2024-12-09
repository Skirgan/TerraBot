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



bot.load = MethodType(load, bot)
