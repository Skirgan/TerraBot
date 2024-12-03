from colorama import Fore, Style

from bot import bot
import discord

import config
from config import Category


def get_channel_id_by_name(guild: discord.Guild, name: str) -> int | None:
    """:return: ID канала, если успешно; None — если безуспешно.
    :param guild: Сервер, внутри которого ищется канал.
    :param name: Имя искомого сервера.
    """

    print(f"{Fore.BLUE}·{Fore.RESET}{Fore.CYAN} Поиск канала {name}...{Fore.RESET}", end="")

    for channel in guild.channels:
        if channel.name == name:
            print(f"{Fore.GREEN} Канал {Style.BRIGHT}{name}{Style.NORMAL} найден.{Fore.RESET}")
            return channel.id

    print(f"{Fore.RED} Канал {Style.BRIGHT}{name}{Style.NORMAL} не найден!{Fore.RESET}")
    return None

def get_role_id_by_name(guild: discord.Guild, name: str) -> int | None:
    """:return: ID роли, если успешно; None — если безуспешно.
    :param guild: Сервер, внутри которого ищется роль.
    :param name: Имя искомого сервера.
    """

    print(f"{Fore.BLUE}·{Fore.RESET}{Fore.CYAN} Поиск роли {name}...{Fore.RESET}", end="")

    for role in guild.roles:
        if role.name == name:
            print(f"{Fore.GREEN} Роль {Style.BRIGHT}{name}{Style.NORMAL} найдена.{Fore.RESET}")
            return role.id

    print(f"{Fore.RED} Роль {Style.BRIGHT}{name}{Style.NORMAL} не найдена!{Fore.RESET}")
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

    print(f"{Fore.RED} Роль {Style.BRIGHT}{name}{Style.NORMAL} не найдена!{Fore.RESET}")
    return None

def override_category_ids(guild: discord.Guild, category: Category(), function: type(get_guild_by_name)):
    # f = list(config["Роли"].keys())
    f = category.__dict__.keys()

    _strings = ""
    for _s in f:
        _strings += f"{Style.BRIGHT}" + _s + f"{Style.NORMAL}, "

    _strings = _strings.removesuffix(", ")

    s = input(f"Введите названия ролей в следующем порядке: {_strings}").split(", ")

    # Пройтись одновременно по всем переменным (var) ролей в конфиге и всем полученным через input() именам (name).
    # Каждую итерацию вызывает необходимую функцию поиска и перезаписывает значение конфига.
    for var, name in zip(f, s):
        __new_id = function(guild, name)
        if __new_id is not None:
            print("Заменяю старое значение на новое... ", end="")

            try:
                # config["Роли"][var] = __new_id
                setattr(category, var, __new_id)

            except Exception as err:
                print(f"{Fore.RED + Style.BRIGHT}Безуспешно:{Style.NORMAL} {err}{Fore.RESET}")
                print(
                    f"{Fore.WHITE + Style.BRIGHT}======== КОНЕЦ ПЕРЕЗАПИСИ КОНФИГА ========{Fore.RESET + Style.NORMAL}\n")
                return False

            else:
                print(f"{Fore.GREEN + Style.BRIGHT}Успешно.{Fore.RESET + Style.NORMAL}")

        else:
            return False

def override_config_ids(guild: discord.Guild) -> bool:
    """:return: bool в зависимости от успеха операции.
    Перезаписывает все ID ролей и каналов на новые, полученные при помощи названий.
    :param guild: Сервер, которому принадлежат ID ролей и каналов, что будут перезаписаны.
    """

    global config

    print(f"\n{Fore.WHITE + Style.BRIGHT}======== ПЕРЕЗАПИСЬ КОНФИГА ========{Fore.RESET + Style.NORMAL} ")
    # _config = dict(config)

    # list() нужен, чтобы при изменении f не изменялся конфиг, иначе for ♥♥♥♥♥♥♥♥♥♥♥♥ и выдаёт ошибку.
    f = list(config["Роли"].keys())
    s = input(f"Введите названия ролей в следующем порядке: {Style.BRIGHT}activist_role_id{Style.NORMAL}, {Style.BRIGHT}administrator_role_id{Style.NORMAL},"
              f" {Style.BRIGHT}master_role_id{Style.NORMAL}, {Style.BRIGHT}moderator_role_id{Style.NORMAL}: ").split(", ")

    # Пройтись одновременно по всем переменным (var) ролей в конфиге и всем полученным через input() именам (name).
    # Каждую итерацию вызывает необходимую функцию поиска и перезаписывает значение конфига.
    for var, name in zip(f, s):
        __new_id = get_role_id_by_name(guild, name)
        if __new_id is not None:
            print("Заменяю старое значение на новое... ", end="")

            try:
                config["Роли"][var] = __new_id

            except Exception as err:
                print(f"{Fore.RED + Style.BRIGHT}Безуспешно:{Style.NORMAL} {err}{Fore.RESET}")
                print(f"{Fore.WHITE + Style.BRIGHT}======== КОНЕЦ ПЕРЕЗАПИСИ КОНФИГА ========{Fore.RESET + Style.NORMAL}\n")
                return False

            else:
                print(f"{Fore.GREEN + Style.BRIGHT}Успешно.{Fore.RESET + Style.NORMAL}")

        else:
            return False

    f = list(config["Каналы"].keys())
    s = input(f"Введите названия каналов в следующем порядке: {Style.BRIGHT}channel_log_delete_id{Style.NORMAL}, {Style.BRIGHT}channel_log_hits_id{Style.NORMAL},"
              f" {Style.BRIGHT}forum_tasks_id{Style.NORMAL}: ").split(", ")

    # Тут так же
    for var, name in zip(f, s):
        __new_id = get_channel_id_by_name(guild, name)
        if __new_id is not None:
            print("Заменяю старое значение на новое... ", end="")

            try:
                config["Каналы"][var] = __new_id

            except Exception as err:
                print(f"{Fore.RED + Style.BRIGHT}Безуспешно:{Style.NORMAL} {err}{Fore.RESET}")
                print(f"{Fore.WHITE + Style.BRIGHT}======== КОНЕЦ ПЕРЕЗАПИСИ КОНФИГА ========{Fore.RESET + Style.NORMAL}\n")
                return False

            else:
                print(f"{Fore.GREEN + Style.BRIGHT}Успешно.{Fore.RESET + Style.NORMAL}")

        else:
            print(f"{Fore.WHITE + Style.BRIGHT}======== КОНЕЦ ПЕРЕЗАПИСИ КОНФИГА ========{Fore.RESET + Style.NORMAL}\n")
            return False

    print(f"{Fore.GREEN + Style.BRIGHT}Перезапись прошла успешно.{Fore.RESET + Style.NORMAL}")
    print(f"{Fore.WHITE + Style.BRIGHT}======== КОНЕЦ ПЕРЕЗАПИСИ КОНФИГА ========{Fore.RESET + Style.NORMAL}\n")
    return True
