from classes import EmojiModes
from colorama import Fore, Style

_indent = " "
s2 = "│"    # ├
color = Fore.WHITE + Style.BRIGHT
color2 = Fore.CYAN

def initialize_config(file):
    """Ничего не возвращает.
    Принимает файл, проходит по всем строкам и пытается записать найденные параметры в словарь, попутно сортируя по категориям.
    Инструкция по использованию находится непосредственно в файле конфига.
    """

    print(f"{color}======== ИНИЦИАЛИЗАЦИЯ КОНФИГА ========{Fore.RESET} ")

    global config
    _config = {}

    # Глубина словаря. Значение заменяет место, куда записываются переменные: так из {<место записи>} можно перейти на {"Роли": {<место записи>}} при необходимости.
    _level = _config    # Работает как указатель, кстати.

    with open(file, "r", encoding="utf-8-sig") as file:    # keyword параметры пишутся слитно с пробелом.

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

                _level[name] = value

                print(f"{color}│{Fore.RESET}")
                print(f"{color}│{Fore.RESET}  Текущий вид словаря: {_config}. Вид _level: {_level}.")    # ╞══
                print(f"{color}│{Fore.RESET}")

                continue

            # Объявляет ли строка категорию имён.
            elif ":" in line:
                print(f"{color}{s2}{_indent*2}─{Fore.RESET} Строка объявляет категорию имён.")

                _level = dict()    # Переназначение _level на пустой словарь.
                _config[line.removesuffix(":\n")] = _level    # Вкладывание _level внутрь конфига.

                print(f"{color}│{Fore.RESET}{_indent} _level перенесён. Текущий вид словаря: {_config}")

            print(f"{color}│{Fore.RESET}")

    print(f"{color}└──────{Fore.RESET} Конец чтения файла.  ")
    return _config

config = initialize_config("config.txt")
print(f"{color}======== КОНЕЦ ИНИЦИАЛИЗАЦИИ КОНФИГА ========{Fore.RESET} ")