import copy

from colorama import Fore, Style
from bot import bot
import discord

#TODO Расставить отступы для читаемости, переписать комментарии и написать их там, где требуется.

def get_channel_id_by_name(guild: discord.Guild, name: str) -> int | None:
    """:return: ID канала, если успешно; None — если безуспешно.
    :param guild: Сервер, внутри которого ищется канал.
    :param name: Имя искомого канала.
    """

    print(f"{Fore.BLUE}·{Fore.RESET}{Fore.CYAN} Поиск канала {name}...{Fore.RESET}", end="")

    for channel in guild.text_channels:
        if channel.name == name:
            print(f"{Fore.GREEN} Канал {Style.BRIGHT}{name}{Style.NORMAL} найден.{Fore.RESET}")
            return channel.id

    print(f"{Fore.RED} Канал {Style.BRIGHT}{name}{Style.NORMAL} не найден!{Fore.RESET}")
    return None

def get_role_id_by_name(guild: discord.Guild, name: str) -> int | None:
    """:return: ID роли, если успешно; None — если безуспешно.
    :param guild: Сервер, внутри которого ищется роль.
    :param name: Имя искомой роли.
    """

    print(f"{Fore.BLUE}·{Fore.RESET}{Fore.CYAN} Поиск роли {name}...{Fore.RESET}", end="")

    for role in guild.roles:
        if role.name == name:
            print(f"{Fore.GREEN} Роль {Style.BRIGHT}{name}{Style.NORMAL} найдена.{Fore.RESET}")
            return role.id

    print(f"{Fore.RED} Роль {Style.BRIGHT}{name}{Style.NORMAL} не найдена!{Fore.RESET}")
    return None

def get_category_id_by_name(guild: discord.Guild, name: str) -> int | None:
    """:return: ID категории, если успешно; None — если безуспешно.
    :param guild: Сервер, внутри которого ищется роль.
    :param name: Имя искомой категории.
    """

    print(f"{Fore.BLUE}·{Fore.RESET}{Fore.CYAN} Поиск категории {name}...{Fore.RESET}", end="")
    for category in guild.categories:
        if category.name == name:
            print(f"{Fore.GREEN} Категория {Style.BRIGHT}{name}{Style.NORMAL} найдена.{Fore.RESET}")
            return category.id

    print(f"{Fore.RED} Категория  {Style.BRIGHT}{name}{Style.NORMAL} не найдена!{Fore.RESET}")
    return None

def get_guild_by_name(name: str) -> discord.Guild | None:
    """:return: discord.Guild, если успешно; None — если безуспешно.
    :param name: Имя искомого сервера.
    """

    print(f"{Fore.BLUE}·{Fore.RESET}{Fore.CYAN} Поиск сервера {name}...{Fore.RESET}", end="")

    for _guild in bot.guilds:
        if _guild.name == name:
            print(f" {Fore.GREEN} Сервер {Style.BRIGHT}{name}{Style.NORMAL} найден.{Fore.RESET}")
            return _guild

    print(f"{Fore.RED} Сервер {Style.BRIGHT}{name}{Style.NORMAL} не найден!{Fore.RESET}")
    return None
