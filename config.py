import copy
import io

from colorama import Fore, Style
import discord

from classes import EmojiModes
from functions import *

# TODO: Переписать комментарии, заменить повсюду обращения к словарю конфига на обращение к объекту конфига.

class Config():
    pass

class Section():
    pass

_indent = " "
s2 = "│"    # ├
color = Fore.WHITE + Style.BRIGHT
color2 = Fore.CYAN

def initialize_config(file):
    """:return: Config структуры Config.Section.переменная = значение
    Принимает файл, проходит по всем строкам и пытается записать найденные параметры в словарь, попутно сортируя по категориям.
    Инструкция по использованию находится непосредственно в файле конфига.
    """

    print(f"{color}======== ИНИЦИАЛИЗАЦИЯ КОНФИГА ========{Fore.RESET} ")

    _config = Config()

    # Глубина словаря. Значение заменяет место, куда записываются переменные: так из {<место записи>} можно перейти на {"Роли": {<место записи>}} при необходимости.
    _level = _config    # Работает как указатель, кстати.
    if isinstance(file, bytes):
        file = io.StringIO(file.decode("utf-8-sig"))
    else:
        file = open(file, "r", encoding="utf-8-sig") # keyword параметры пишутся слитно с пробелом.
        

    
    try:    # мне лень с вима убирать все отступы, так что да. Потом уберу возможно.
        print(f"{color}┌──────{Fore.RESET} Начало чтения файла. ")
        print(f"{color}│{Fore.RESET}")

        for line in file.readlines():

            print(f"{color}├─{Fore.RESET} Читаю строку: {color2}\"{line.removesuffix("\n")}\"{Fore.RESET}.")

            # Является ли строка комментарием.
            if line.startswith("#"):
                print(f"{color}{s2}{_indent*2}─{Fore.RESET} Строка является комментарием.")
                print(f"{color}│{Fore.RESET}")
                continue

            # Объявляет ли строка переменную.
            elif " = " in line:
                print(f"{color}{s2}{_indent*2}─{Fore.RESET} Строка объявляет переменную.")

                line = line.split(" = ")    # Делит строку на название переменной и её значение; защита от дурака не предусмотрена.

                name = line[0]
                print(f"{color}{s2}{_indent*2}─{Fore.RESET} Имя переменной —{color2}", name+f"{Fore.RESET}.")

                value = line[1].removesuffix("\n")
                print(f"{color}{s2}{_indent*2}─{Fore.RESET} Значение переменной —{color2} \""+value+f"\"{Fore.RESET}.")

                # Преобразовать значение в число, если возможно.
                try:
                    value = int(value)

                # Не число.
                except ValueError:
                    print(f"{color}{s2}{_indent*2}─{Fore.RESET} Переменная не является числом.")

                    # Если значение не является числом и не объявляется как строка, то, либо это enum, либо кодер ♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥.
                    if value[0] not in ["\"", "\'"] and "." in value:    # Если первый символ не является кавычками и значение имеет точку.
                        print(f"{color}{s2}{_indent*2}─{Fore.RESET} Переменная является enum.")

                        # Пока enum в конфиге один, потому только его и ожидаем.
                        # Пройтись по аттрибутам EmojiModes.
                        print(f"{color}{s2}{_indent*2}─{Fore.RESET} Цикл по аттрибутам Emojimodes:")

                        for mode in EmojiModes:
                            print(f"{color}{s2}{_indent*4}─{Fore.RESET} {mode}")

                            # Если значение совпадает с названием аттрибута, заменяем значение на аттрибут.
                            if value.split(".")[1] == mode.name:
                                print(f"{color}{s2}{_indent*6}─{Fore.RESET} Значение совпадает с данным именем. Заменяю его на аттрибут.")

                                value = mode
                                break

                    else:    # Если строка или bool.
                        if value == "True":
                            value = True

                        elif value == "False":
                            value = False

                        else:
                            value = value.removeprefix("\"").removesuffix("\"")   # Убираю кавычки из строки. Кавычки у нас по конвенции, не полноценный компилятор делаю же.

                print(f"{color}{s2}{_indent}{Fore.RESET} Записываю.")

                setattr(_level, name, value)
                #    _level[name] = value

                # print(f"{color}│{Fore.RESET}")
                # print(f"{color}│{Fore.RESET}  Текущий вид словаря: {_config}. Вид _level: {_level}.")    # ╞══
                print(f"{color}│{Fore.RESET}")

                continue

            # Объявляет ли строка категорию имён.
            elif ":" in line:
                print(f"{color}{s2}{_indent*2}─{Fore.RESET} Строка объявляет категорию имён.")
                name = line.removesuffix(":\n")
                setattr(_config, name, Section())
                _level = getattr(_config, name)
                #    _level = dict()    # Переназначение _level на пустой словарь.
                #    _config[line.removesuffix(":\n")] = _level    # Вкладывание _level внутрь конфига.

                # print(f"{color}│{Fore.RESET}{_indent} _level перенесён. Текущий вид словаря: {_config}")

            print(f"{color}│{Fore.RESET}")
    
    except Exception as e:
        print(e)

    print(f"{color}└──────{Fore.RESET} Конец чтения файла.  {Style.NORMAL}")

    file.close()
    return _config

config = initialize_config("config.txt")
print(f"{color}======== КОНЕЦ ИНИЦИАЛИЗАЦИИ КОНФИГА ========{Fore.RESET}{Style.NORMAL}\n")

def override_config(file):
    global config
    config = initialize_config(file)

def read_config():
    """:return: Void
    Выводит аттрибуты конфига, аттрибуты аттрибутов конфига и их значения в консоль в читаемом виде.
    """
    global config
    for name, value in config.__dict__.items():
        print()
        print(f"Категория \"{name}\"")
        for name, value in value.__dict__.items():
            print(f"{name}: {value}")

def override_section_ids(guild: discord.Guild, section: Section(), function: type(get_guild_by_name)):
    # f = list(config["Роли"].keys())
    f = section.__dict__.keys()

    _strings = ""
    for _s in f:
        _strings += f"{Style.BRIGHT}" + _s + f"{Style.NORMAL}, "

    _strings = _strings.removesuffix(", ")

    s = input(f"Введите названия в следующем порядке: {_strings}: ").split(", ")

    # Пройтись одновременно по всем переменным (var) ролей в конфиге и всем полученным через input() именам (name).
    # Каждую итерацию вызывает необходимую функцию поиска и перезаписывает значение конфига.
    for var, name in zip(f, s):
        # print(f"Пытаюсь найти объект с именем {Style.BRIGHT}{name}{Style.NORMAL}...", end = " ")
        __new_id = function(guild, name)
        if __new_id is not None:
            print(f"Заменяю старое значение {Style.BRIGHT}{var}{Style.NORMAL} на новое... ", end=" ")

            try:
                # config["Роли"][var] = __new_id
                setattr(section, var, __new_id)

            except Exception as err:
                print(f"{Fore.RED + Style.BRIGHT}Безуспешно:{Style.NORMAL} {err}{Fore.RESET}")
                
                return False

            else:
                print(f"{Fore.GREEN + Style.BRIGHT}Успешно.{Fore.RESET + Style.NORMAL}")

        else:
            # print(f"{Fore.RED + Style.BRIGHT}Безуспешно:{Style.NORMAL} не удалось найти объект.{Fore.RESET}")
            return False
    return True


def override_config_ids(guild: discord.Guild) -> bool:
    """:return: bool в зависимости от успеха операции.
    Перезаписывает все ID ролей и каналов на новые, полученные при помощи названий.
    :param guild: Сервер, которому принадлежат ID ролей и каналов, что будут перезаписаны.
    """

    print(f"\n{Fore.WHITE + Style.BRIGHT}======== ПЕРЕЗАПИСЬ КОНФИГА ========{Fore.RESET + Style.NORMAL} ")
    # _config = dict(config)

    global config
    _config = copy.deepcopy(config)

    if \
    override_section_ids(guild, _config.roles, get_role_id_by_name) and \
    override_section_ids(guild, _config.channels, get_channel_id_by_name) and \
    override_section_ids(guild, _config.categories, get_category_id_by_name):

        # for debug purposes
        config = copy.deepcopy(_config)
        read_config()   
        return True
    
    i = input("Перезапись конфига прервана. Использовать неизменённый конфиг (y/yes) или начать сначала (enter)?\n").lower() 
    if i == "y" or i == "yes":
        return False
        print(f"{Fore.WHITE + Style.BRIGHT}======== КОНЕЦ ПЕРЕЗАПИСИ КОНФИГА ========{Fore.RESET + Style.NORMAL}\n")
    
    override_config_ids(guild)

# read_config(config)
# print(config.Каналы.forum_tasks_id)
