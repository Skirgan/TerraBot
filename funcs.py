from bot import bot

def get_channel_id_by_name(guild, name):
    for channel in guild.channels:
        if channel.name == name:
            return channel.id
    return None

def get_role_id_by_name(guild, name):
    for role in guild.roles:
        if role.name == name:
            return role.id
    return None

def get_guild_by_name(name):
    for _guild in bot.guilds:
        if _guild.name == name:
            return _guild
    print(f"Сервер {name} не найден!")
    return False


def override_config_ids(guild):
    """Ничего не возвращает.
    Перезаписывает все ID ролей и каналов на новые, полученные при помощи названий.
    :return: bool в зависимости от успеха операции.
    """
    from config import config

    f = list(config["Роли"].keys())
    s = input("Введите названия ролей в следующем порядке: activist_role_id, administrator_role_id, master_role_id, moderator_role_id: ").split(", ")

    for var, name in zip(f, s):
        __new_id = get_role_id_by_name(guild, name)
        if __new_id is not None:
            print("До:", config["Роли"][var])
            config["Роли"][var] = __new_id
            print("После:", config["Роли"][var])
        else:
            print(f"Роль {name} не найдена!")
            return False

    f = list(config["Каналы"].keys())
    s = input("Введите названия каналов в следующем порядке: channel_log_delete_id, channel_log_hits_id, forum_tasks_id: ").split(", ")

    for var, name in zip(f, s):
        __new_id = get_channel_id_by_name(guild, name)
        if __new_id is not None:
            config["Каналы"][var] = __new_id
        else:
            print(f"Канал {name} не найден!")
            return False
    return True