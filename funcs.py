from bot import bot

def get_channel_id_by_name(guild, name):
    for channel in guild.channels:
        if channel.name == name:
            return channel
    return None

def get_role_id_by_name(guild, name):
    for role in guild.roles:
        if role.name == name:
            return role
    return None

def override_config_ids(guild_name):
    """Ничего не возвращает.
    Перезаписывает все ID ролей и каналов на новые, полученные при помощи названий.
    :return: bool в зависимости от успеха операции.
    """
    from config import config
    for _guild in bot.guilds:
        if _guild.name == guild_name:
            guild = _guild
        else:
            print(f"Сервер {guild_name} не найден!")
            return False
    for var, name in config["Роли"].keys, input("Введите названия ролей в следующем порядке: activist_role_id, administrator_role_id, master_role_id, moderator_role_id").split(", "):
        __new_id = get_role_id_by_name(guild, name)
        if __new_id is not None:
            config["Роли"][name] = __new_id
        else:
            print(f"Роль {name} не найдена!")
            return False
    for var, name in config["Каналы"].keys, input("Введите названия каналов в следующем порядке: channel_log_delete_id, channel_log_hits_id, forum_tasks_id").split(", "):
        __new_id = get_channel_id_by_name(guild, name)
        if __new_id is not None:
            config["Каналы"][name] = __new_id
        else:
            print(f"Канал {name} не найден!")
            return False
    return True